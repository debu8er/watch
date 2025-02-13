<h1 align="center">watch</h1>
<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#tool-options">Tool options</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

watch is a tool for watching subdomain and save details in database(MongoDB)

## Installation
* install MongoDB on local https://www.mongodb.com/docs/manual/installation/
* ```bash
  git clone https://github.com/debu8er/watch.git
  cd watch
  pip install -r requirements.txt
  python3 main.py
  ```

### Tool Options
* `sub` : It show subdomain
* `status` : It show subdomain statuses
* `tech` : It show subdomain technology
* `status_changed` : The statuses that show changing
* `tech_changed` : The technologies that show changing
* `fresh` : This will be true if it is a new subdomain
* `timestamp` : Time of first subdomain registration



## Usage
Simple usage:
```bash
python3 main.py
```


## License
This project is licensed under the MIT license. See the LICENSE file for details.
