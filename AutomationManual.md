### Automating your API calls ###
#### -- It's actually very simple. ###

1. Create your script.py file

2. In your terminal environment, type in
  crontab -e

3. This will open up a text editor for you. Depending on your computer setting, different Linux text editor may be called.

4. In this text editor you opened, type/copy in the following two lines

  ```
  PATH="placeholder explained below"

  0 0 * * * python3 '/your directory/script.py'
```
5. You need to find out where your PATH should be - essentially the environment where your Python is installed. To do so, go back to your terminal or open up a new terminal window and type in:
  ``` Bash
  echo $PATH
  ```

  The returned result is what you would put in the placeholder above for PATH.

6. The second line tells your machine to run the script you specified at 0:00 everyday.

7. For testing, set a time in the next few minutes so you can see if the cron works as intended.

8. Once you are done creating the crontab file, save and exit it out using
the editor specific commands. For vim, you can use Shift+zz.

9. You have scheduled your Python jobs!
