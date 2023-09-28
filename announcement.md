# Maintenance mode

Status will not receive new features, only bug fixes.


### Why?

I don't like Python package management. It's often problematic when running on a bare-metal system and makes app installation much harder for inexperienced users. I want to give up on using virtual environments and try something new.

You say Docker? Yes, but it's not a complete solution. Status mainly reads files from `/proc`, `/sys` and various storage devices, thus it means greater access permissions are required. We probably need to create our own `docker-compose.yml` file to match the machine we use.


### Solution? `Go` for it!

The solution is simple. Fully functional, single executable static binary with all resources already included. What if you download **just one file** and run it with **just one command**?

Yes, I am going to rewrite Status again, but this time in `Go`.


### Planned features

- probably all features available now

- multi instance support

- server-side auth

- refreshed UI

- setup wizard

These are certainties. Definitely, will be more.


-----


Thanks everyone for being here and checking out this project.

**Stay tuned!**
