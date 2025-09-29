import json
import statistics

def detect_outliers(data):
    high_performers = []
    at_risk = []
    recommendations = []

    for emp in data['employees']:
        dept = emp['department']
        scores = emp['quarterly_scores']
        dept_avg = data['department_averages'][dept]
        if all(s > a*1.1 for s,a in zip(scores, dept_avg)):
            high_performers.append({'employee_id': emp['employee_id'], 'reason':'Consistently 10% above dept avg', 'confidence':0.85})
        if len(scores) >=2 and (scores[-1] < scores[-2]*0.85):
            at_risk.append({'employee_id': emp['employee_id'], 'reason': f'{int((scores[-2]-scores[-1])/scores[-2]*100)}% decline over 2 quarters', 'confidence':0.92})
            recommendations.append({'employee_id': emp['employee_id'], 'action':'Schedule performance improvement plan meeting', 'priority':'high'})

    return {'high_performers': high_performers, 'at_risk': at_risk, 'recommendations': recommendations}

# Example usage
if __name__ == "__main__":
    with open("sample_data.json") as f:
        data = json.load(f)
    result = detect_outliers(data)
    print(json.dumps(result, indent=4))
