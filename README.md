# Ansible Syncope Collection

## Test module logic

1. First make sure to edit in a proper way the following conf files:
   - `./plugins/modules/syncope_change_user_status/args.json`
   - `./plugins/modules/syncope_change_user_status/playbook_conf.yml` 

1. Test the module logic by running one the following 2 options:
    1. from the `./plugins/modules/syncope_change_user_status`:
       ```sh
       python -m syncope_change_user_status args.json
       ```
       > `-m [MODULE_NAME]`:
       >
       > the name of the module must be equals to the name 
       > of the `plugins/modules/syncope_change_user_status` folder 
     
    2. with Playbook:
       ```sh
       ansible-playbook -M . ./playbook_conf.yml
       ```
 
1. Install [Mazer CLI](https://galaxy.ansible.com/docs/mazer/install.html#latest-stable-release)
    ```sh
    pip3 install mazer
    ```

1. Edit `galaxy.yml` properly and use `mazer` to build and publish the collection
    ```sh
    ~/.local/bin/mazer build
    
    ~/.local/bin/mazer publish --api-key=SECRET ./releases/my_namespace-syncope-1.0.0.tar.gz
    ```
