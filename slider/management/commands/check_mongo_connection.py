from django.core.management.base import BaseCommand
from mongoengine import connection

class Command(BaseCommand):
    help = "Check MongoDB connection status"

    def handle(self, *args, **kwargs):
        try:
            # Check the default connection
            conn = connection.get_connection()
            # If the connection is successful, print the host info
            self.stdout.write(self.style.SUCCESS(f"Connected to MongoDB at: {conn.address}"))
        except Exception as e:
            # Print the error if connection fails
            self.stdout.write(self.style.ERROR(f"Failed to connect to MongoDB: {str(e)}"))
