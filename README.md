# Ansible Syncope Collection

## Test module logic

1. First make sure to edit the file `plugins/modules/syncope_change_user_status/args.json` 
according to your needs.

1. Test the module logic by running:
    ```sh
    python -m changeUserStatus args.json
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
