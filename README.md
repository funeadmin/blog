various features:  
I want to create a blog site, and bio for myself, and I want to have a place where my wife can share places we have traveled to, as well as share images. 
  
Various endpoints:  This will be a work in progress, I want to copy the workflow used for the twitter assignment back in SQL class. 
As I dive back in forth I will continue to add. For now, I will add the below:  
 base_url/Users : GET : liking_shouts 
            : DEL delete 
            : POST create 
 base_url/Shouts: GET : liking_users 
                             : DEL delete 
                             : POST create 
base_url/articles
 
The database, will be a Postgres database, below is the DB name, including column names, data types, constraints, and foreign keys. I attached an ER diagram as well. 

DB :  Holla 
Tables :  
           likes  :   user_id, shout_id, create_at
           constraints:  likes_shout_id_fkey, digs_user_id_fkey 
           shouts:   id, content, create_at, user_id
           Contraints:  shouts_user_id_fkey, shouts_pkey 
           users :  id, username, password 
           Contraints :  users_key, users_username_key 
