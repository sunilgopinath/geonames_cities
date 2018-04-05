@Singleton
class Database:
  connection = None
  def get_connection(self):
    if self.connection is None:
      self.connection = MySQLdb.connect(host="localhost", user="root", passwd="razvan", db="mydatabase")
    return self.connection