from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np

class PerformanceOutlierAPIView(APIView):
    """
    POST endpoint to analyze employee performance data and identify high performers,
    at-risk employees, underperformers, and goal achievement issues.
    """

    def post(self, request):
        data = request.data
        employees = data.get("employees", [])
        dept_avg = data.get("department_averages", {})

        high_performers = []
        at_risk = []
        underperformers = []
        goal_issues = []
        recommendations = []

        for emp in employees:
            emp_id = emp["employee_id"]
            dept = emp["department"]
            scores = emp["quarterly_scores"]
            goals = emp.get("goal_completion_rates", [])

            # Skip if data incomplete
            if not scores or dept not in dept_avg:
                continue

            dept_scores = dept_avg[dept]
            # High performers: consistently above dept average (+10%)
            above_count = sum(1 for s, d in zip(scores, dept_scores) if s > 1.1*d)
            if above_count >= len(scores)//2:
                high_performers.append({
                    "employee_id": emp_id,
                    "reason": "Consistently above department average",
                    "confidence": round(above_count/len(scores),2)
                })

            # At-risk: performance drop >15% over 2+ quarters
            for i in range(1, len(scores)):
                drop = (scores[i-1] - scores[i])/scores[i-1]
                if drop > 0.15:
                    at_risk.append({
                        "employee_id": emp_id,
                        "reason": f"{round(drop*100)}% performance decline over 2 quarters",
                        "confidence": round(drop,2)
                    })
                    recommendations.append({
                        "employee_id": emp_id,
                        "action": "Schedule performance improvement plan meeting",
                        "priority": "high"
                    })
                    break

            # Underperformers: >1 std below dept average
            mean = np.mean(dept_scores)
            std = np.std(dept_scores)
            for s in scores:
                if s < mean - std:
                    underperformers.append({
                        "employee_id": emp_id,
                        "reason": "Performance significantly below department average",
                        "confidence": round((mean-s)/std,2)
                    })
                    break

            # Goal achievement issues: consistently <60%
            if goals and all(g < 0.6 for g in goals):
                goal_issues.append({
                    "employee_id": emp_id,
                    "reason": "Consistently low goal completion (<60%)",
                    "confidence": 1.0
                })
                recommendations.append({
                    "employee_id": emp_id,
                    "action": "Review goal planning and provide support",
                    "priority": "medium"
                })

        result = {
            "high_performers": high_performers,
            "at_risk": at_risk,
            "underperformers": underperformers,
            "goal_issues": goal_issues,
            "recommendations": recommendations
        }

        return Response(result, status=status.HTTP_200_OK)
