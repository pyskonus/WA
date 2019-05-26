# I did not include the files needed to extend the dictionary here, because
# they can't be sent into GitHub repo. Due to this, the distribution can not
# have the possibility to extend the dictionary.


from distutils.core import setup


setup(name='Word associations',
      version='0.0.2',
      description='Word associations dictionary for Ukrainian language',
      author='Bohdan Pysko',
      author_email='pyskob190201@gmail.com',
      url='https://github.com/pyskonus/WA',
      pu_modules=['data_preparation.main', 'interaction.main',
                  'investigation_modules.add_to_dict',
                  'investigation_modules.bigraph',
                  'investigation_modules.bigraph_test',
                  'investigation_modules.use_bigraph_example'],
      data_files=[('results', ['results/inc.list', 'results/RESULT.json'])])
