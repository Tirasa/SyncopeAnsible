  # README.md

  # Ansible Syncope Collection

  ## Test module logic

  1. From the base directory execute the unit test:
      ```sh
         python -m pytest tests/
        ```
  1. Make sure to edit in a proper way the following conf files:
       `./plugins/modules/args.json`
       `./tests/integration/targets/syncope_user_handler/tasks/main.yml`

  1. Test the module logic by running one of the following 2 options:
      1. Providing a json file:
         from the `./plugins/modules/` directory run
         ```sh
         python -m syncope_user_handler args.json
         ```
         > `-m [MODULE_NAME]`:
         >
         > the name of the module must be equals to the name
         > of the `plugins/modules/syncope_user_handler` class

      2. With Playbook:
         from the base directory:
         ```sh
         ansible-test integration
         ```
         > executing ansible test requires the collection be in a specific path:
         >
         > `/ansible_collections/{namespace}/SyncopeAnsible/`


  ## Pushing a new version
  1. Build the collection artifact: ansible-galaxy collection build

  1. Publish the collection artifact: ansible-galaxy collection publish ./geerlingguy-php_roles-1.2.3.tar.gz --api-key=[key goes here]

