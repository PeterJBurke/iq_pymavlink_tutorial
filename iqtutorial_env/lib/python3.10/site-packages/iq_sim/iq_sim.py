import os
import requests
import json
import sys
import time

class iq_sim: 
    
    def __init__(self, token: str):
        if os.getenv("IQ_SIM_ENV") == "dev":
            self.url = "http://localhost/sim/api/v1/"
        else:
            self.url = "https://intelligentquads.com/sim/api/v1/"


        self.headers = {'token': token}
        # get sim capabilities from API
        self.sim_capabilities = self.get_sim_capabilities()
        self.define_default_sim_config()

    def define_default_sim_config(self):
        self.sim_config = {
            "sim_config": [
                {
                    "sim_type": "default-sitl",
                    "vehicle_type": "ArduCopter",
                    "vehicle_model": "X",
                    "instances": "1",
                    "flight_controls": "Ardupilot",
                    "fc_version": self.sim_capabilities["flight_controls"]["Ardupilot"]["simulation"]["default-sitl"]["vehicle_types"]["ArduCopter"]["version_default"],
                    "latlonaltheading": [
                        "-35.363261",
                        "149.16523",
                        "584",
                        "353"
                    ]
                }
            ]
        }
    def get_sim_capabilities(self):
        """gets the capabilities of the Intelligent Quads cloud simulation service

        Returns:
            Dict: dict containing information of the different simulation options available
        """        
        r = requests.get(self.url + 'capabilities', headers=self.headers)
        result = json.loads(r.text)
        if "error" in result:
            print(result["error"])
            sys.exit(1)
        else:
            return result

    def get_running_simulations(self, sim_id: str = None):
        """gets a list of running simulations for a user
            if providing a sim_id, will return only return info for that sim_id

        Args:
            sim_id (str, optional): unique id of a simulation. Defaults to None.

        Returns:
            Dict: dict in form of {"running_sims": [{"status": str, "sim_id": str, "fc_instances": str, "creation_time" : str}]}
        """
        r = requests.post(self.url + 'running_sims', headers=self.headers)
        print(r.text)
        result = json.loads(r.text)
        if "error" in result:
            print(result["error"])
            sys.exit(1)
        else:
            if sim_id is None:
                return result
            else:
                for sim in result["running_sims"]:
                    if sim["sim_id"] == sim_id:
                        print(sim)
                        return sim
                return None

    def stop_sim(self, sim_id: str):
        """stop a simulation running in the Intelligent Quads cloud
            will exit 1 if there is an error
        Args:
            sim_id (str): sim_id of the simulation to stop

        Returns:
            Dict: dict in form of {"status": str, "sim_id": str}
        """
        r = requests.post(self.url + 'stop', json={"sim_id": sim_id}, headers=self.headers)
        result = json.loads(r.text)
        if "error" in result:
            print(result["error"])
            sys.exit(1)
        else:
            return result

    def stop_all_sims(self):
        """Stops all of a users simulations running in the Intelligent Quads cloud

        Returns:
            List: list of dicts in form of {"status": str, "sim_id": str}
        """
        r = requests.post(self.url + 'stop', headers=self.headers, json={"stop_all": True})
        print(r)
        result = json.loads(r.text)
        if "error" in result:
            print(result["error"])
            sys.exit(1)
        else:
            return result


    def start_sim(self, sim_config=None) -> str:
        """create a new simulation running in the Intelligent Quads cloud

        Args:
            sim_config (Dict, optional): configuration for the simulation.

        Returns:
            str: sim_id of the simulation
        """

        if sim_config is None:
            sim_config = self.sim_config

        # This is the request that you want to send to the API
        r = requests.post(self.url + 'start', json=sim_config, headers=self.headers)
        print(r)
        print(r.text)
        result = json.loads(r.text)
        print(result)

        if "status" in result and result["status"] == "success":
            sim_id = result["sim_id"]
            print(f"sim_id: {sim_id}")
            return sim_id
            
        else:

            print("failed")
            print(result)
            sys.exit(1)

    def get_connection(self, sim_id: str):
        """get the ip address and port of the mavlink interface running in the Intelligent Quads cloud

        Args:
            sim_id (str): unique id of the simulation

        Returns:
            Dict: dict in form of {"status": str, "ip": str, "port": int}
        """        
        r = requests.post(self.url + 'get_connection', json={"sim_id": sim_id}, headers=self.headers)
        result = json.loads(r.text)
        if result["status"] == "error":
            print(result["error"])
            sys.exit(1)
        else:
            return result
    
    def wait_for_sim_ready(self, sim_id: str, timeout: int = 80):
        """wait for the simulation to be deployed and running in the Intelligent Quads cloud
            Note: During High Traffic times, it can take up to a couple of minutes to start a simulation. 
            try setting timeout higher or try again later.

            function will exit 1 if the simulation fails to start

        Args:
            sim_id (str): unique id of the simulation
            timeout (int, optional): Defaults to 80.
        """        
        time_start = time.time()
        while time.time() - time_start < timeout:
            result = self.get_running_simulations(sim_id)
            print(result)
            if result:
                if result["status"] == "Running":
                    return
                else:
                    time.sleep(1)
            else:
                time.sleep(1)

        print("timed out waiting for sim to start. During High Traffic times, it can take up to a couple of minutes to start a simulation. try setting timeout higher or try again later.")   
        sys.exit(1)