# Demo Script

Target length: 2 to 3 minutes.

## 0:00 - 0:20 Problem

Reservation mobility is not only about finding a car. Operators need to know why a fare was generated, why a driver was or was not assigned, whether a driver is restricted, and whether the system is safe to intervene in.

On screen: show the demo console title and the order selector.

## 0:20 - 0:55 Normal Order

Select `trip_demo_001` and click Explain Order.

Narration: This order has a trusted route, a passenger fare, a driver income breakdown, and an eligible driver. The Copilot explains the assignment and keeps the evidence visible.

## 0:55 - 1:35 Dispatch Exception

Select `trip_demo_002` and click Explain Order, then Recommend Action.

Narration: The order is blocked because no eligible online driver remains after dispatch filtering. The Copilot can recommend redispatch, but it does not execute the action by itself.

## 1:35 - 2:10 Human Approval

Select `trip_demo_003`, click Recommend Action, then Approve Last Action.

Narration: This driver is available, but reservation dispatch is limited. The Copilot recommends manual driver restriction review. The operator explicitly approves, and the audit log records the AI recommendation separately from the human decision.

## 2:10 - 2:40 System Evidence

Click Explain System.

Narration: GBA Go also includes sanitized evidence from a pre-existing backend production certification: a 20 QPS x 3600 second run with 72,000 completed requests, 72,000 successful requests, zero timeouts, zero state inconsistencies, and a TSS of 3.849986. This demo includes only the sanitized summary, not production hostnames, credentials, or user data.

## 2:40 - 3:00 Closing

Narration: GBA Go Operations Copilot is not a generic chatbot. It is an AI operations layer for reservation mobility, designed to explain system decisions, support precise human intervention, and keep high-risk actions auditable.
