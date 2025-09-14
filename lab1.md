# Lab 1: Setting Up Your Lab Environment

## Objectives

By the end of this lab, you will:

1. Create a GitHub account and verify your student status.
2. Understand the GitHub Student Developer Pack and its benefits.
3. Use GitHub Codespaces to run Python code directly in the browser (no local setup required).
4. Write and run simple Python programs using input() and print().

___  

### Part 1: Create Your GitHub Account

1. Go to https://github.com
2. Click Sign up and create a new account using your university email address.
3. Choose a username you’re comfortable using throughout your degree (avoid joke names).
4. Use a strong password (consider a password manager).
5. Verify your email address by clicking the link GitHub sends you.

___  

### Part 2: Verify as a Student

1. Visit GitHub Education
2. Click Get Student Benefits.
3. Log in with your GitHub account.
4. Apply for the GitHub Student Developer Pack:
5. Provide your university email (if not already used).
6. Upload proof of student status (Clear picture of your student ID card ).
7. Secure your account using two-factor authentication
8. Complete your user profile/billing information.. essentially your name as it appears on your student ID, and your address (no need to add credit cards etc.)
9. Wait for approval (usually within 24–48 hours).

> 💡 You can continue with the rest of this lab without waiting for approval.

___  

### Part 3: Explore GitHub Codespaces

GitHub Codespaces lets you run code in the cloud with just a browser — no need to install Python locally.

1. Log into GitHub
2. Create a new repository:
3. Click the + in the top-right corner → New repository.
4. Name it: lab-01.
5. Choose Public (you can make it private later if you prefer).
6. Check Add a README file.
7. Click Create repository.
8. On the repository page, click the green Code button → Open with Codespaces → New codespace.
9. After a short wait, you’ll have a full coding environment running in your browser.(Will open a new tab)

> :writing_hand: You can use the README File each week to keep any notes you want for each lab.

___  

### Part 4: Your First Python Program

In your Codespace, create a new file:  
1. In the Explorer panel, click New File.
2. Name it hello.py.
3. Type the following code:  
   ```print("Hello, world!")```

Run it by typing this command in the terminal at the bottom:  
```python3 hello.py```

You should see:  
```Hello, world!```

___  

### Part 5: Using Input and Print

Now let’s make your program interactive. Replace the contents of hello.py with:

```name = input("What is your name? ")```
```print("Hello, " + name + "!") ```

Run it again:  
```python3 hello.py```

> Try typing different names. What happens?

___  

### Part 6: Practice Exercises

1. Write a program that asks the user for their age, then prints:  
   > You are X years old.

2. Write a program that asks the user for two numbers, adds them, and prints the result.
   
3. Write a program that asks a students for their name, age and student number and then print that information back out.

___  

###  Deliverables

By the end of this lab, you should:

Have a GitHub account and repository named lab-01.
Be able to run Python code in Codespaces.

___  

### Further Work 

In your second lab this week we'll be learning more basic python commands and completing more practice exercises.  
Feel free to [explore codespaces](https://www.datacamp.com/tutorial/github-codespaces), any intro to [python courses](https://www.w3schools.com/python/), or even [look at using markdown](https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet) for your notes. (you can look at the source of this page for some basic examples)


