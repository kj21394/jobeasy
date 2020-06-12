# jobeasy

# usage 

## Running it from terminal:
## The arguments to run the program
### url - seek, jora (TODO), indeed (TODO)
### feilds - list of position to apply (eg: ['engineer', 'data-analyst', 'software-engineer']). NOTE: remember to sepatrate two words with '-' rater than space.
### location - place to apply (takes only one string argument, default = 'All-Australia')
### pages - percentage of pages to extrace data from (eg: '50')
### ignore - list words in the title that you want to exclude like senior or intenship (eg: ['senior','internship', 'part-time'])
### citizen - if want data of jobs for require candidate to be a citizen (take True or False as the argument)
### To run: python jobs.py -url 'seek' -feilds ['engineer', 'data-analyst', 'software-engineer'] -location 'All-Australia' -pages '50' -ignore ['senior','internship', 'part-time'] -citizen False