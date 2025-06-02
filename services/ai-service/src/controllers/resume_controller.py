import json
import random
import string
import traceback
from typing import Dict, Optional, Tuple

import numpy as np
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ..services.resume_analyzer_service import PracticalResumeAnalyzer
from ..services.query_service import generate_query_engine
from ..templates.resume_template import TEMPLATE
from ..templates.jd_template import JD_TEMPLATE

from ..utils.text_util import advanced_ats_similarity, clean_text
from ..services.recommendation_service import getRecommendations


class ResumeController:
    def __init__(self):
        self.analyzer = PracticalResumeAnalyzer()

    def _convert_to_normal_types(self, data: Dict) -> Dict:
        """Convert numpy types to native Python types."""
        new_data = {}
        for key, value in data.items():
            if isinstance(value, np.generic):
                new_data[key] = value.item()
            elif isinstance(value, dict):
                new_data[key] = self._convert_to_normal_types(value)
            elif isinstance(value, list):
                new_data[key] = [item.item() if isinstance(item, np.generic) else item for item in value]
            else:
                new_data[key] = value
        return new_data

    def _process_resume_documents(self, documents) -> str:
        """Combine all document texts into a single string."""
        return "".join(doc.text_resource.text for doc in documents)

    def _process_job_description(self, jd: str) -> Dict:
        """Process job description into a dictionary."""
        jd_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        query_engine_jd, documents_jd = generate_query_engine(
            jd, jd_id, read_from_text=True, jd=True
        )

        if not query_engine_jd or not documents_jd:
            raise HTTPException(status_code=400, detail="Query engine for job description failed")

        response_jd = query_engine_jd.query(JD_TEMPLATE)
        response_jd = clean_text(response_jd.response)
        return json.loads(response_jd)

    def _calculate_scores(self, resume_dict: Dict, job_description_dict: Dict, resume_str: str) -> Dict:
        """Calculate all scores for the resume analysis."""
        technical = advanced_ats_similarity(resume_dict, job_description_dict)
        technical = self._convert_to_normal_types(technical)

        grammar_score, recommendations, section_scores, justifications = self.analyzer.analyze_resume(
            resume_str, resume_dict, industry=job_description_dict['industry']
        )

        overall_score = (technical["similarity_score"] * 0.55 + grammar_score * 0.45)
        overall_score = min(round(overall_score, 2), 100)

        return {
            "overall_score": overall_score,
            "technical_score": technical,
            "grammar_analysis": {
                "score": grammar_score,
                "recommendations": recommendations,
                "section_scores": section_scores,
            },
            "justifications": justifications,
            "resume_data": dict(resume_dict),
        }

    def analyze_resume(self, abs_path: str, jd: str, resume_id: str) -> JSONResponse:
        """Main method to analyze a resume against a job description."""
        try:
            # Process resume documents
            query_engine, documents = generate_query_engine(abs_path, resume_id, read_from_text=False)
            if not query_engine or not documents:
                raise HTTPException(status_code=400, detail="Failed to process documents")

            resume_str = self._process_resume_documents(documents)

            # Get resume data
            response = query_engine.query(TEMPLATE)
            response = clean_text(response.response)
            resume_dict = json.loads(response)

            # Process job description
            try:
                job_description_dict = self._process_job_description(jd)
            except Exception as e:
                print(f"Error processing job description into dictionary: {e}")
                traceback.print_exc()
                raise HTTPException(
                    status_code=500,
                    detail="Error processing job description into dictionary"
                )

            # Calculate scores
            analysis_results = self._calculate_scores(resume_dict, job_description_dict, resume_str)

            # Add recommendations
            refined_out = getRecommendations(analysis_results)
            analysis_results.update(refined_out)

            return JSONResponse(content=analysis_results, status_code=200)

        except json.JSONDecodeError as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=400,
                detail=f"Error decoding resume data: {e}. Ensure your resume format is correct."
            )
        except HTTPException:
            raise  # Re-raise HTTPExceptions
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Error processing resume: {e}"
            )
