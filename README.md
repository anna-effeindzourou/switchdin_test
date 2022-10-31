<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

 In this project we set up a broker with RabbitMQ. I am deploying it in a docker container.
 Then, we have a three applications to publish and consume messages using Python. 
 Before starting the applications make sure you have the following installed:
- ```
    Docker
    ```  
- ```
    Docker Compose
    ```
### Installation

Instruction for the installation and setting up of this project.

2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install packages:
   ```
    pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
1. RunRabbitMQ in docker container:
   2. docker compose up
3. Start the following scripts:
   3. ```python publish_random_number.py  ```
   4.    ```python publish_stats.py  ``` 
   5.    ```python display_stats.py  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

