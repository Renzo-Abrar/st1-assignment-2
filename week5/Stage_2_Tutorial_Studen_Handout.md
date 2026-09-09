# Assignment 2 Case Study: Stage 2 Tutorial - From Problems to Requirements

## Activity 1 - Stakeholder Map

| Stakeholder | Need                                                          | Potential Conflict                                                                                     |
|---|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Receptionist** | Quick patient lookup with appointment scheduling | Prefers simple, fast interface over multi step verification                                            
| **Practitioner (Doctor/Nurse)** | Accurate patient history and clear daily appointment schedules | Needs detailed patient history without clutter from cancelled appointments.                            |
| **Clinic Manager / Management** | Reliable  tracking and historical appointments | Wants full record retention/audit trails which may clutter operational views if unfiltered.            |
| **Patient** | Efficient booking process and clear status updates | Desires convenience (e.g., self-service/reminders) which may fall outside immediate core system scope. |

## Activity 2 - Functional or Non-Functional?

- [x] **Functional** [ ] Non-functional — The system shall allow staff to cancel an appointment.
- [ ] Functional [x] **Non-functional** — The system should remain responsive for the course-scale dataset.
- [x] **Functional** [ ] Non-functional — The system shall retain cancelled appointments.
- [ ] Functional [x] **Non-functional** — Core business logic should be independently testable.
- [x] **Functional** [ ] Non-functional — The system shall search for a patient by ID.

---

## Activity 3 - Repair Ambiguous Requirements

1. **"The system should be easy to use."**
   - **Problem:** "Easy to use" is pretty subjective and isn't really measurable/testable.
   - **Clarification question:** What specific usability metric (e.g., task completion time under 30 seconds for new staff with zero training) defines acceptable ease of use?

2. **"Patient search should be fast."**
   - **Problem:** "Fast" is pretty vague and depends on the hardware and data size.
   - **Clarification question:** What is the maximum acceptable query response time in seconds for searching patient records under normal load?

3. **"The system should securely manage data."**
   - **Problem:** "Securely manage" doesn't specify any security controls, encryption, or access standards.
   - **Clarification question:** What specific authentication, authorization level, and data protection standards must be applied to patient data?

4. **"Appointments should normally be easy to cancel."**
   - **Problem:** "Normally" is an ambiguous rule, and "easy" is unmeasurable.
   - **Clarification question:** Under what conditions can an appointment be cancelled, and what rules restrict cancellations?

---

## Activity 4 - AI Requirements Audit

| AI Suggestion | Classification | Evidence / Reason                                                                               |
|---|---|-------------------------------------------------------------------------------------------------|
| **Patients receive SMS reminders.** | Out of scope | Brief specifies internal staff usage, no mention of external SMS integration.                   |
| **Facial recognition login.** | Out of scope | Unsupported highly complex, exceeds basic system requirements.                                  |
| **Receptionists create appointments.** | Confirmed | Brief  mentions receptionists/staff managing appointments and schedule difficulties.            |
| **Online payment.** | Out of scope | Brief focuses strictly on patient, practitioner, and appointment tracking—no financial requirements. |
| **Practitioners view schedules.** | Confirmed | Brief lists practitioners as primary users needing clear schedule visibility.                   |
| **AI recommends treatments.** | Unsupported | Unsupported capability, client requested a tracking system, not decision support.               |
| **Cancelled appointments remain in history.** | Confirmed | Brief does request retention of appointment history and status inconsistency.         |

---

## Exit Question

**Why is 'AI suggested it' not sufficient evidence for a requirement?**

Ai models generate suggestions that are based on pattern recognition rather than actual client needs. So Accepting AI suggestions without any sort of verification poses risks, non existent business rules and features that the client wouldnt need or support. Requirements must be grounded in verified project documentation and for stakeholder evidence. 

