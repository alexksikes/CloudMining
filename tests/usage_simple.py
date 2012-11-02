from cloudmining import CloudMiningApp

# assumes a default directory structure
app = CloudMiningApp.from_directory('.')

# launch default web server
if __name__ == '__main__':
    app.run()
