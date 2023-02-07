import csv


def save_to_csv(jobs):
    file = open('data.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['title', 'company', 'metro', 'link'])
    for job in jobs:
        writer.writerow(list(job.values()))
    return