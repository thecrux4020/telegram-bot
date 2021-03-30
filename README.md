[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/thecrux4020/telegram-bot">
    <img src="images/logo.jpg" alt="Logo">
  </a>

  <h3 align="center">Telegram Polls</h3>

  <p align="center">
    Simple bot to send quizzes to telegram channel
    <br />
    <a href="#how-it-works"><strong>Explore how it works »</strong></a>
    <br />
    <br />
    <a href="https://github.com/thecrux4020/telegram-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/thecrux4020/telegram-bot/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#how-it-works">How It Works</a>
      <ul>
        <li><a href="#polls-job">Polls Job</a></li>
        <li><a href="#infrastructure">Infrastructure</a></li>
        <li><a href="#project-structure">Project Structure</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- HOW IT WORKS -->
## How It Works
<br />
<p align="center">
    <img src="images/how-it-works.png" alt="how-it-works">
</p>
<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
The bot supports 2 different operational modes, _jobs_ and _webhooks_:

* **Jobs** is designed to run specific tasks, like a crontab job in linux, but the example above is a serverless job. 
* **Webhooks** is designed to handle events (messages, audios, images, etc) from telegram. When something happens in the channel, or someone send something to the bot.

___

Different jobs could run in different lambda functions, or in different environments (for example, a docker image on linux). Each job has a configuration section inside `settings.ini`, where you can configure all the variables related to it.

Usually, each job has a storage associated with, in the case of polls-job, the storage is a dynamodb table, where all the polls/quizzes are stored. 

Each job has a cloudwatch event rule, that triggers the job in a specific point in time, for example, every day at 09:00 AM.

___

### Polls Job

Polls are a way that telegram has to send quizzes or questions to a channel. You can send a quizz with multiple answer, or just a quiz with one correct answer. After you answer to the quiz, you can see the statistics of it.

Example: 

<p align="center">
    <img src="images/quiz.jpeg" alt="quiz-example-telegram" width=500 height=300>
</p>

The job has a dynamodb table where job manager (you!) store all the questions that want to send to the channel. With the help of a cloudwatch rule lambda function trigger in a specific time of the day, take one question from the dynamodb table, send it to the channel and update the status of the quiz.

The table has a field calle `has_been_used`; this field is used to avoid send the same question multiple times. The lambda function selects a question randomly, and after send to the channel, mark the question as used.

___

### Infrastructure

Inside iac/ path, you'll find the **terraform** files needed to deploy the infrastructure inside AWS, but if you want, you can host the bot wherever you like; You just need to adjust the config file and run `main.py`, like other python apps (don't forget installing dependencies and setting environment variables).

___

### Project Structure

- **app**: _source code of the app_
    - **helpers**: _common functions_
    - **jobs**: _all the jobs, each job has one class_
    - **repository**: _classes for interact with storage_
- **iac**: _terraform files_
    - `main.tf`: _configuration stuff_
    - `poll_job.tf`: _poll job infrastructure definition_
    - `provider.tf`: _provider configuration_
    - `variables.tf`: _variables used in code_
- **images**: _images for README.md_
- **scripts**: _usefull scripts_
    - `build.sh`: _generate build file to deploy in lambda (run before deploy in terraform)_
- `settings.ini`: _configuration file_
- `main.py`: _main file of the app, all setup stuff of python app_
- `requirements.txt`: _dependencies file_

___

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png