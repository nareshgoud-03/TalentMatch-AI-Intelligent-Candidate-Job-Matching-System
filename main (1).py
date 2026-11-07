import pandas as pd
import numpy as np

def match_candidates(candidates_path, jobs_path, output_path):
    
    try:
        candidates = pd.read_csv(candidates_path)
        jobs = pd.read_csv(jobs_path)
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return

    candidates['clean_skills'] = candidates['skills'].fillna('').astype(str).str.lower()
    candidates['skills_set'] = candidates['clean_skills'].apply(
        lambda x: {s.strip() for s in x.split('|') if s.strip()}
    )



    jobs['clean_skills'] = jobs['required_skills'].fillna('').astype(str).str.lower()
    jobs['skills_set'] = jobs['clean_skills'].apply(
        lambda x: {s.strip() for s in x.replace('\n', ' ').split(' ') if s.strip()}
    )

    results = []

    for _, job in jobs.iterrows():
        job_id = job['job_id']
        job_skills = job['skills_set']
        
        job_matches = []
        for _, cand in candidates.iterrows():
            cand_id = cand['candidate_id']
            cand_skills = cand['skills_set']
            
            
            intersection = job_skills.intersection(cand_skills)
            score = len(intersection)
            
            
            if score > 0:
                matched_skills_list = sorted(list(intersection))
                explanation = f"Matched {score} skill(s): {', '.join(matched_skills_list)}."
            else:
                explanation = "No matching skills found."
                
            job_matches.append({
                'job_id': job_id,
                'candidate_id': cand_id,
                'score': float(score),
                'explanation': explanation
            })
            
        
        job_matches_df = pd.DataFrame(job_matches)
        
        
        
        job_matches_df = job_matches_df.sort_values(
            by=['score', 'candidate_id'], 
            ascending=[False, True]
        ).reset_index(drop=True)
        
        
        top_5 = job_matches_df.head(5).copy()
        top_5['rank'] = range(1, len(top_5) + 1)
        
        results.append(top_5)
        
    
    final_results = pd.concat(results, ignore_index=True)
    final_results = final_results[['job_id', 'candidate_id', 'rank', 'score', 'explanation']]
    final_results.to_csv(output_path, index=False)
    print(f"Successfully generated {output_path} with {len(final_results)} rows.")

if __name__ == '__main__':
    match_candidates(
        candidates_path='/content/candidate_profiles.csv',
        jobs_path='/content/job_descriptions.csv',
        output_path='results.csv'
    )
