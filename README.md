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

- Clone the repo:
   ```sh
   git clone https://github.com/anna-effeindzourou/switchdin_test.git
   ```
- Install packages:
   ```
    pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
- Run RabbitMQ in docker container:
  -  ```docker compose up ```
- Start the following scripts:
   -  ```python publish_random_number.py```    
   -  ```python publish_stats.py  ```
   - ```python display_stats.py  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


