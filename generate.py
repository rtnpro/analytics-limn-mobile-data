import os
import sys
import glob
import MySQLdb as mysql
from jinja2 import Template
import yaml
import limnpy

conn = mysql.connect("s1-analytics-slave.eqiad.wmnet", "research", os.environ["RESEARCH_PASSWORD"], "log")
#conn = mysql.connect("s1-analytics-slave.eqiad.wmnet", read_default_file=os.path.expanduser('~/.my.cnf.research'), db="log")

def execute(sql):
    cur = conn.cursor()
    cur.execute(sql)
    return cur

def render(template, env):
    t = Template(template)
    return t.render(**env)

if __name__ == "__main__":
    if len(sys.argv) != 2: #FIXME: argparse please
        print "Usage: generate.py <folder with config.yaml and *.sql files>"
        sys.exit(-1)

    folder = sys.argv[1]
    config = yaml.load(open(os.path.join(folder, "config.yaml")))
    graphs = dict([
        (   os.path.basename(filename).split(".")[0], 
            render(open(filename).read(), config)
        ) for filename in glob.glob(os.path.join(folder, "*.sql"))
    ])
    for key, sql in graphs.items():
        print "Generating %s" % key
        rows = execute(sql)
        headers = [field[0] for field in rows.description]
        ds = limnpy.DataSource(limn_id=key, limn_name=key, data=list(rows), labels=headers, date_key='Date')
        ds.__source__['url'] = ds.__source__['url'].replace("/data/datafiles", "/data/datafiles/mobile") # EEEK UGLY HACK!
        ds.write(basedir='.')
        ds.write_graph(basedir='.')
