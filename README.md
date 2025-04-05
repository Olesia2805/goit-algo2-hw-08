#

=== Simulating the flow of messages ===
---
Message's number|  User  |     Allowed?    |
----------------|--------|-----------------|
Message  1      | User 2 | ✓ 
Message  2      | User 3 | ✓ 
Message  3      | User 4 | ✓ 
Message  4      | User 5 | ✓ 
Message  5      | User 1 | ✓ 
Message  6      | User 2 | × (waiting 7.0s)
Message  7      | User 3 | × (waiting 7.2s)
Message  8      | User 4 | × (waiting 7.2s)
Message  9      | User 5 | × (waiting 8.0s)
Message 10      | User 1 | × (waiting 8.1s)

---
Waiting 4 seconds...
---

=== New series of messages after waiting ===
---
Message's number|  User  |     Allowed?    |
----------------|--------|-----------------|
Message 11      | User 2 | × (waiting 1.0s)
Message 12      | User 3 | × (waiting 0.6s)
Message 13      | User 4 | × (waiting 0.0s)
Message 14      | User 5 | × (waiting 0.5s)
Message 15      | User 1 | × (waiting 0.3s)
Message 16      | User 2 | ✓
Message 17      | User 3 | ✓
Message 18      | User 4 | ✓
Message 19      | User 5 | ✓
Message 20      | User 1 | ✓