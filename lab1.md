# Lab 1: Setting Up Your Lab Environment

## Objectives

By the end of this lab, you will:

1. Create a GitHub account and verify your student status.
2. Understand the GitHub Student Developer Pack and its benefits.
3. Use GitHub Codespaces to run Python code directly in the browser (no local setup required).
4. Write and run simple Python programs using input() and print().


### Part 1: Create Your GitHub Account

1. Go to https://github.com
2. Click Sign up and create a new account using your university email address.
3. Choose a username you’re comfortable using throughout your degree (avoid joke names).
4. Use a strong password (consider a password manager).
5. Verify your email address by clicking the link GitHub sends you.

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


All of the lab activities and in-class demos will be completed using the setup outlined below, however you are free to use any setup and tools you prefer. 
> :warning: I won't be troubleshooting any issues on different setups, outside of the suggested lab environment. 

___

## Recommended Lab Setup:

1. VirtualBox hypervisor 
2. Kali Linux VM  
-- recommended, but any modern linux VM should be fine
___

Download:
VirtualBox: [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads) (Download the package for your own OS)  
Kali Linux image (latest version): [https://www.kali.org/get-kali/](https://www.kali.org/get-kali/) (For most students, I'm recommending the pre-built virtual box image)  


## Setup Instructions 


1. Install VirtualBox - Run the downloaded installer and follow the on-screen instructions.
   
2. Extract the Kali VirtualBox image.
> ⚠️ The downloaded image file is a 7zip compressed archive, so you'll first need to extract the VirtualBox image before importing to Virtualbox.  
   
   -- On windows you can download the offical 7zip app to extract the image. [https://www.7-zip.org/](https://www.7-zip.org/)  
   -- On Linux you can type ```7z x filename.7z```  
   -- On Mac the default archive tool should be able to extract the image.  

4. Start VirtualBox and select ‘Add’. We then navigate to the location our VM is downloaded and find the .vbox file.
5. You can change any of the settings to suit your own system, and then start the VM.
   > 💡 Base Memory: Allocate a minimum of 2048 MB RAM (more for better performance).  
   > 💡 Processors: 1 CPU (more for better performance)

> :writing_hand: The default login is kali for the user and kali for the password!

6. Update your kali, Open a terminal and run: ```sudo apt update && sudo apt upgrade```




Part 3: Explore GitHub Codespaces

GitHub Codespaces lets you run code in the cloud with just a browser — no need to install Python locally.

Log into GitHub
.

Create a new repository:

Click the + in the top-right corner → New repository.

Name it: lab-01.

Choose Public (you can make it private later if you prefer).

Check Add a README file.

Click Create repository.

On the repository page, click the green Code button → Open with Codespaces → New codespace.

After a short wait, you’ll have a full coding environment running in your browser.

Part 4: Your First Python Program

In your Codespace, create a new file:

In the Explorer panel, click New File.

Name it hello.py.

Type the following code:

print("Hello, world!")


Run it by typing this command in the terminal at the bottom:

python3 hello.py


You should see:

Hello, world!

Part 5: Using Input and Print

Now let’s make your program interactive.

Replace the contents of hello.py with:

name = input("What is your name? ")
print("Hello, " + name + "!")


Run it again:

python3 hello.py


Try typing different names. What happens?

Part 6: Challenge Exercises

Write a program that asks the user for their age, then prints:

You are X years old.


Write a program that asks the user for two numbers, adds them, and prints the result.

(Optional) Create a new file madlib.py that asks for several words (noun, verb, adjective) and prints a silly sentence using them.

Deliverables

By the end of this lab, you should:

Have a GitHub account and repository named lab-01.

Be able to run Python code in Codespaces.

Submit your repository link to the assignment page on the LMS.

👉 Would you like me to format this into a student handout PDF with screenshots (step-by-step visuals), or keep it as text instructions for now?

You said:
text instructions are preferred but could you include step-by-step visuals with the text?
ChatGPT said:

Perfect — we can make this a hybrid lab guide: clear text instructions plus simple inline visuals (screenshots, icons, arrows, etc.) so your students aren’t lost at each step. I’ll structure it so the visuals are suggestions for where you can paste in screenshots, and you can later capture them yourself (or I can mock up placeholders for you).

Here’s the upgraded lab handout draft:

Lab 1: Setting Up Your Lab Environment
Objectives

By the end of this lab, you will:

Create a GitHub account and verify your student status.

Understand the GitHub Student Developer Pack and its benefits.

Use GitHub Codespaces to run Python code directly in the browser.

Write and run simple Python programs using input() and print().

Part 1: Create Your GitHub Account

Go to https://github.com
.
(Screenshot: GitHub homepage)

Click Sign up in the top-right corner.
(Screenshot: “Sign up” button highlighted)

Fill in the details:

Username → choose something professional.

Email → use your university email address.

Password → strong and unique.
(Screenshot: GitHub sign-up form)

Verify your email by clicking the link GitHub sends you.
(Screenshot: sample verification email)

Part 2: Verify as a Student

Visit GitHub Education
.
(Screenshot: GitHub Education page)

Click Get Student Benefits.
(Screenshot: “Get Student Benefits” button highlighted)

Log in with your GitHub account.

Apply for the Student Developer Pack:

Provide your university email.

Upload proof of enrollment (e.g., student card).
(Screenshot: application form)

Approval usually takes 24–48 hours, but you can continue with this lab.

Part 3: Explore GitHub Codespaces

Log into GitHub.

Click the + icon in the top-right → New repository.
(Screenshot: “+” dropdown menu)

Fill in the repository details:

Name: lab-01

Select: Add a README file
(Screenshot: new repository form)

On the repository page, click the green Code button → Codespaces tab → New codespace.
(Screenshot: “Code” button with Codespaces tab open)

Wait a moment while your Codespace launches — it will look like VS Code running in your browser.
(Screenshot: Codespaces environment with editor + terminal)

Part 4: Your First Python Program

In the left-hand Explorer panel, click New File → name it hello.py.
(Screenshot: new file creation in Explorer)

Type the following code:

print("Hello, world!")


(Screenshot: code typed into editor)

Run the file in the terminal below:

python3 hello.py


(Screenshot: terminal showing “Hello, world!” output)

Part 5: Using Input and Print

Replace your program with this:

name = input("What is your name? ")
print("Hello, " + name + "!")


Run it again:

python3 hello.py


Test with different names.
(Screenshot: example run with user typing “Alice” → “Hello, Alice!”)

Part 6: Challenge Exercises

Try these on your own:

Ask for the user’s age and print:

You are X years old.


Ask for two numbers, add them, and print the result.

(Optional) Create madlib.py: ask for several words (noun, verb, adjective) and print a silly sentence.

(Screenshot: optional madlib program running with funny sentence)

Deliverables

A GitHub repository named lab-01.

At least two working Python files (hello.py and your own challenge).

Submit your repository link via the LMS.
