# Sends notifications if price goes above certain threshold.

To run, create a file named .env (A file to store your environment variable)
Set the value of COINMARKET_API_KEY equal to a string with your api key.

You can always add onto the program with adding sms notifications with Twillio (I currently don't have money to test it out), or adding email notifications which is quite pointless. Fun things you could do would be to store the prices and date and then plotting it with mathplotlib.