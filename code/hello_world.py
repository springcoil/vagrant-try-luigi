import luigi

# this, does exactly nothing except for printing a message
class HelloWorldTask(luigi.Task):
    task_namespace = 'testing'

    def run(self):
        print("{task} says: Hello world!".format(task=self.__class__.__name__))

if __name__ == '__main__':
    # run it locally, without submitting to the Luigi daemon
    #luigi.run(['testing.HelloWorldTask', '--workers', '1', '--local-scheduler'])
    luigi.run(['testing.HelloWorldTask'])

