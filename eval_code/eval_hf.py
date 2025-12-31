import json
from collections import defaultdict
from typing import List, Dict, Any
from tabulate import tabulate
import re

def preprocess_answer(answer: str, yes_or_no=False) -> str:
    if not isinstance(answer, str):
        return None
    if yes_or_no == False:
        match = re.search(r"^([A-F])[\W\s_]*", answer.upper())
        return match.group(1).upper() if match else None
    else:
        match = re.search(r"^(yes|no)[\W\s_]*", answer.lower(), re.IGNORECASE)
        return match.group(1) if match else None
    
    return answer

def calculate_metrics(json_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Calculate metrics for each test subset
    """
    # Store statistics for each test subset
    subset_stats = defaultdict(lambda: {
        'total': 0,
        'correct': 0,
        'accuracy': 0.0
    })
    
    # Process each data item
    for item in json_data:
        # Extract subset name
        full_id = item.get('id', '')
        if ':' in full_id:
            subset_name = full_id.split(':')[0]
        else:
            subset_name = full_id
        
        # Get prediction and ground truth
        prediction = item.get('prediction', '')
        gt_answer = item.get('gt_answer', '')
        
        # Preprocess answers
        yes_or_no = gt_answer.strip().lower() in ['yes', 'no']
        processed_pred = preprocess_answer(prediction, yes_or_no)
        processed_gt = preprocess_answer(gt_answer, yes_or_no)
        
        # Update statistics
        subset_stats[subset_name]['total'] += 1
        
        # Check if correct (handle empty string cases)
        if processed_pred and processed_gt:
            is_correct = processed_pred == processed_gt
            if is_correct:
                subset_stats[subset_name]['correct'] += 1
    
    # Calculate accuracy
    for subset in subset_stats:
        total = subset_stats[subset]['total']
        correct = subset_stats[subset]['correct']
        subset_stats[subset]['accuracy'] = correct / total if total > 0 else 0.0
    
    return dict(subset_stats)

def calculate_weighted_average(stats: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate weighted average metrics
    """
    total_samples = 0
    weighted_sum = 0.0
    
    for subset_name, subset_data in stats.items():
        total = subset_data['total']
        accuracy = subset_data['accuracy']
        
        total_samples += total
        weighted_sum += accuracy * total
    
    weighted_avg = weighted_sum / total_samples if total_samples > 0 else 0.0
    
    return {
        'total_samples': total_samples,
        'weighted_accuracy': weighted_avg
    }

def display_results_table(stats: Dict[str, Dict[str, Any]], weighted_avg: Dict[str, Any]):
    """
    Display results using tabulate format
    """
    # Prepare table data
    table_data = []
    headers = ["Test Subset", "Total Samples", "Correct", "Accuracy"]
    
    # Add data for each test subset
    for subset_name, subset_data in sorted(stats.items()):
        table_data.append([
            subset_name,
            subset_data['total'],
            subset_data['correct'],
            f"{subset_data['accuracy']:.4f} ({subset_data['accuracy']*100:.2f}%)"
        ])
    
    # Add separator row
    table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])
    
    # Add summary data
    table_data.append([
        "Total / Weighted Average",
        weighted_avg['total_samples'],
        "N/A",
        f"{weighted_avg['weighted_accuracy']:.4f} ({weighted_avg['weighted_accuracy']*100:.2f}%)"
    ])
    
    # Output table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Output detailed statistics
    print("\nDetailed Statistics:")
    print(f"Total samples: {weighted_avg['total_samples']}")
    print(f"Number of test subsets: {len(stats)}")
    print(f"Weighted average accuracy: {weighted_avg['weighted_accuracy']:.4f} ({weighted_avg['weighted_accuracy']*100:.2f}%)")

def process_json_file(json_file_path: str):
    """
    Process JSON file and calculate metrics
    """
    try:
        # Read JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f"Successfully read JSON file: {json_file_path}")
        print(f"Total entries: {len(json_data)}")
        
        # Calculate metrics
        subset_stats = calculate_metrics(json_data)
        
        # Calculate weighted average
        weighted_avg = calculate_weighted_average(subset_stats)
        
        # Display results
        display_results_table(subset_stats, weighted_avg)
        
        # Return results for further processing
        return {
            'subset_stats': subset_stats,
            'weighted_avg': weighted_avg
        }
        
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' does not exist")
    except json.JSONDecodeError as e:
        print(f"Error: JSON file format is incorrect - {e}")
    except Exception as e:
        print(f"Error: An error occurred while processing the file - {e}")

if __name__ == "__main__":
    # json_file_path = "example.json"
    import sys

    result = process_json_file(json_file_path=sys.argv[1])