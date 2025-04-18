<h1 align="center" style="background-color: white; color: orange; padding: 10px; border-radius: 5px; font-weight: bold; font-family: 'Arial', sans-serif;">
  <span style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">CampusStay</span> 
</h1>

## 🔭 *1. Project Description*
*CampusStay 🏠 is a smart hostel management platform designed to support inclusive and efficient student housing, especially for international students on campus. Our mission is to simplify accommodation processes by offering a secure, user-friendly, and fully accessible solution for universities and students alike. Whether it’s assigning rooms, tracking student stays, or managing hostel infrastructure, CampusStay ensures seamless coordination between Student Affairs, and Students removing hassle, promoting fairness, and creating a welcoming campus experience for all.*

- ### *What Does Edupathway Do?*
*CampusStay 🏠 is an accessible hostel management platform designed to streamline student accommodation on campus. It empowers staff to assign rooms to students, view all buildings and current occupants, and monitor key statistics across hostels. With the ability to open or close buildings, add students individually or in bulk via CSV, and manage student records, including deletions, Campus Stay simplifies the entire housing process.*
- ### *Technologies used*
<p align="center"> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.mysql.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" alt="mysql" width="40" height="40"/> </a>  <a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg" alt="bootstrap" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a>  </p>


*We used Linux as the operating system for its stability, Python (Flask) for its simplicity in building scalable web applications, and MySQL for efficient data management. we use Bootstrap, HTML5, CSS3, and JavaScript enable a responsive, dynamic, and interactive front-end experience. Git helps with collaboration throughout the development process.*
## 🛠️ *2. Installation Steps*
*⚠️ Ensure that the technologies listed above are installed before proceeding with the installation steps, as it won't work otherwise!*

*1. Clone the repository*

```bash
git clone https://github.com/antoineleno/porfolio
```

*2. Change the working directory*

```bash
cd porfolio
``` 

*3. Create and activate the virtual environment*

```bash
python3 -m venv myenv; source myenv/bin/activate
```

*4. Install dependencies*

```bash
pip install -r requirements/requirements.txt
```
*5. Set up the database*
```bash
sudo mysql -u root -p < requirements/set_up_db.sql
sudo mysql -u root -p < requirements/campus_dev_db_backup.sql
```
*6. Create hostel for male and female using the console*
```bash
cd; cd porfolio; CAMPUS_TYPE_STORAGE=db python3 console.py
```

```bash
create Hostel hostel_type="Male"
```
```bash
create Hostel hostel_type="Female"
```
```bash
quit
```

*7. Change the working directory and Run the app*

```bash
cd; cd porfolio/web_flask; CAMPUS_TYPE_STORAGE=db python3 app.py
```

🌟 You are all set!


## 📘  *How to use this project*
*After completing the installation steps, an admin user will be created with the following credentials :*
> - ***username***&nbsp;: *campusstay*
> - ***password*** : *campusstaypassword*

## 🔐 Login Instructions

Visit the following link and enter the credentials provided above to be connected as admin:

👉 [Campusstay Login](http://127.0.0.1:5000/campusstay/login)
> Tip: Right-click the link and choose "Open in new tab" for easier access.

## 👯 *3. Code Contributors*

<p align="center">
  <a href="https://github.com/antoineleno/final_porfolio/graphs/contributors">
    <img src="web_flask/auth/static/images/leno.png" alt="Profile Picture" style="width: 140px; height: 140px; border-radius: 50%; object-fit: cover; margin-right: 20px;">
    <img src="web_flask/auth/static/images/bah.png" alt="Profile Picture" style="width: 140px; height: 140px; border-radius: 50%; object-fit: cover;">
  </a>
</p>

> ### 📫 *How to reach us*
<p align="center">
  <strong>Antoine LENO</strong> &nbsp;&nbsp;&nbsp;&nbsp; <strong>Amadou BAH</strong><br>
  <a href="mailto:lenoantoine2000@gmail.com">
      <img src="web_flask/auth/static/images/email.png" alt="Instagram" height="20" width="20" /></a>
    <a href="https://github.com/antoineleno">
      <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg" alt="Instagram" height="20" width="20" /></a>
  <a href="https://instagram.com/antoineleno7" target="_blank">
    <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="Instagram" height="20" width="20"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="mailto:bamadodu634@gmail.com">
    <img src="web_flask/auth/static/images/email.png" alt="Instagram" height="20" width="20" /></a>
    <a href="https://github.com/Amadou001">
      <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/github.svg" alt="Instagram" height="20" width="20" /></a>
  <a href="https://instagram.com/amadou4176" target="_blank">
    <img src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/instagram.svg" alt="Instagram" height="20" width="20" />
  </a>
</p>


##  *4. Console*
> Run the command below to launch the console, and refer to the documentation for available commands.
```bash
cd; cd porfolio; CAMPUS_TYPE_STORAGE=db python3 console.py
```

## 🏅 *5. Badge*
<p align="center">
  <a href="https://github.com/antoineleno/EduPathway/fork" target="blank">
    <img src="https://img.shields.io/github/forks/antoineleno/EduPathway?style=flat-square" alt="aEduPathway forks"/>
  </a>
  <a href="https://github.com/antoineleno/EduPathway/stargazers" target="blank">
    <img src="https://img.shields.io/github/stars/antoineleno/EduPathway?style=flat-square" alt="EduPathway stars"/>
  </a>
  <a href="https://github.com/antoineleno/EduPathway/issues" target="blank">
    <img src="https://img.shields.io/github/issues/antoineleno/EduPathway?style=flat-square" alt="EduPathway issues"/>
  </a>
  <a href="https://github.com/antoineleno/EduPathway/pulls" target="blank">
    <img src="https://img.shields.io/github/issues-pr/antoineleno/EduPathway?style=flat-square" alt="EduPathway pull-requests"/>
  </a>
  <!-- Example Contribution Badge -->
  <a href="https://github.com/antoineleno/EduPathway/graphs/contributors" target="blank">
    <img src="https://img.shields.io/github/contributors/antoineleno/EduPathway?style=flat-square" alt="EduPathway contributors"/>
  </a>
</p>
