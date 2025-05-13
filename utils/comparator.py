import pandas as pd

# Load the salary benchmark data
def load_benchmarks():
    return pd.read_csv('data/salary_benchmarks.csv')

# Compare extracted salary with benchmark data
def compare_salary(extracted_salary, job_role, location, industry=None):
    benchmarks = load_benchmarks()

    # Filter the benchmark data based on job role and location
    benchmark = benchmarks[(benchmarks['Job Role'] == job_role) & (benchmarks['Location'] == location)]
    
    if industry:
        benchmark = benchmark[benchmark['Industry'] == industry]
    
    if not benchmark.empty:
        min_salary = benchmark['Min Salary'].values[0]
        max_salary = benchmark['Max Salary'].values[0]
        
        # Compare extracted salary with benchmark range
        if extracted_salary < min_salary:
            return f"Below benchmark. The salary is lower than the minimum of ${min_salary}."
        elif extracted_salary > max_salary:
            return f"Above benchmark. The salary is higher than the maximum of ${max_salary}."
        else:
            return f"Within benchmark. The salary is within the range of ${min_salary} to ${max_salary}."
    else:
        return "No benchmark available for the given job role, location, and industry."
