RING REDIS
===

what for:
---

I want a lightweight, High Available & Extensible cache solution using redis, but nutcracker is too heavy for a system with only 2 application server and 2 redis instance. and there isnt a good enough implementation of consistant hash using pure python. so I wrote this. I used it in 2 project and they are running well till now when half a year passed. so I shared it for people who have the same requirement.

features:
---

- lightweight & pure python solution
- O(log(slice_number)) time complexity for a hash calculation. (slice_number = k * node_number, k equal to 200 as default)
- O(slice_number * log(slice_number)) time complexity for hash ring rebuilding.
- use O(slice_number) memory space always.
- only dict like operation supported.

how to use:
---


