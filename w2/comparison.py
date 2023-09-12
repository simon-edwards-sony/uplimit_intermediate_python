import subprocess
import argparse
import time
from pprint import pprint
from global_utils import make_dir
from datetime import datetime
import json

def main():

    # Parse the arguements
    parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
    parser.add_argument('--type',
                        default='all',
                        choices=['tst', 'sml', 'bg', 'all'],
                        help='Type of data to generate')
    args = parser.parse_args()

    # Default testing on all datatypes
    dtypes = ['tst','sml','bg'] if args.type not in ['tst','sml','bg'] else [args.type]
    
    # Weeks to compare
    weeks = ['w1', 'w2']

    # Run the main() method from each work and pass the data type to the method
    output = []
    for dtype in dtypes:
        for week in weeks:
            try:
                starttime = time.time()
                subprocess.run(["python", f"../{week}/main.py", "--type", dtype], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                endtime = time.time()
                print(f"Time taken for \"{dtype}\" data using the \"{week}\" main() method: {endtime-starttime}")
                output.append({
                    'code': week,
                    'dtype': dtype,
                    'secs': endtime-starttime
                })
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
            except FileNotFoundError:
                print("Error: The 'main.py' script was not found.")
    
    # Output the data
    make_dir('../output/comparison')
    with open(f'../output/comparison/{datetime.now().strftime("%B %d %Y %H-%M-%S")}.json', 'w') as f:
        f.write(json.dumps(output, indent = 2))

    pprint(output)

if __name__ == "__main__":
    main()