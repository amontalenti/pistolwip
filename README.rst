Pistol WIP!
===========

Pistol WIP! is a tool for managing work-in-progress (WIP) using Pivotal Tracker
as the backend. It's written in Python using Flask and the pyvotal module.

Though Pivotal Tracker is generally a great tool for managing *team capacity*,
it is somewhat poor at monitoring *individual capacity*. That is, it is
needlessly difficult to "balance" stories out among team members, and to get a
sense of whether "engineer XYZ is overloaded / lightly loaded at this point in
time". This gets even worse if you have more than one Pivotal Tracker project.

The point of Pistol WIP! is to provide an alternative frontend on your Pivotal
Tracker projects that is focused on individuals. They can log into this to get
a sense of their own work, and others can log in to see how lightly /
overloaded other individuals are. It is also meant to help managers with
balancing work among team members, and being able to predict when a certain
individual will be free for backlogged work.
