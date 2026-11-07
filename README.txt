RUN COMMAND:
python main.py

DEPENDENCIES:
- pandas
- numpy

MATCHING APPROACH:
1. Standardizes both job requirements and candidate skills to lowercase.
2. Parses candidate skills (pipe-separated '|') and job requirements (space-separated) into Python sets.
3. Calculates matching score based on set intersection size (number of matching skills).
4. Creates a detailed 'explanation' summarizing which exact skills matched.
5. Handles ranking ties deterministically by sorting alphabetically by candidate_id.

ASSUMPTIONS:
- Missing skill entries are treated as empty skill sets.
- All candidate matching candidates are sorted alphabetically to break score ties consistently.

LIMITATIONS:
- Basic keyword overlap matching does not account for synonyms, skill proficiency levels, or semantic meaning.
- Experience years are not factored into the basic scoring.

QUALITY EVALUATION:
- One way to evaluate quality is to compute Mean Average Precision (MAP) or Normalized Discounted Cumulative Gain (NDCG) against a manually annotated test set of ideal candidate-to-job matches.
