import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

fname = "_data/prs.json"
with open(fname, 'r') as fh:
    data = json.loads(fh.read())
    
merged_prs = [d for d in data if d['node']['state'] == 'MERGED']
merge_dates = np.array([r['node']['mergedAt'] for r in merged_prs], dtype=np.datetime64)
fig, ax = plt.subplots()
h, date_bedges, _ = ax.hist(mdates.datestr2num(merge_dates), bins=(8*12+7));
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
fig.autofmt_xdate()

ax.set_title('Merged PRs over time')
ax.set_xlabel('Time')
ax.set_ylabel('# Merged PRs / 15 days')

plt.show()

# First time contributors vs. time

first_time_contributor = []
prev_contrib = set()
for record in merged_prs:
    try:
        author = record['node']['author']['login']
    except TypeError:  # Author no longer has GitHub account
        first_time_contributor.append(True)
        continue
    if author not in prev_contrib:
        first_time_contributor.append(True)
        prev_contrib.add(author)
    else:
        first_time_contributor.append(False)
# Object dtype for handling None
first_time_contributor = np.array(first_time_contributor, dtype=object)
