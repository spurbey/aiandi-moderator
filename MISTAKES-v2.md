# Clef Mistakes (comments-v2.json)

Model used: `clef`

### Comment 17
- **Comment ID:** 17
- **Author:** Tejas Patil
- **Comment:** "If this API times out one more time I swear I'm going to commit a crime 😤 Killed the script for the 20th time today 💀"
- **Clef's label:** toxic
- **Correct label:** acceptable (borderline)
- **Why:** This is a frustration for prolonged error and thus this seems acceptable instead of toxic but as for community this seems toxic, so yeah i guess clef also understood this and has scored acceptable and toxic at similar range.


### Comment 20
- **Comment ID:** 20
- **Author:** Sana Sheikh
- **Comment:** "Ma'am, someone posted "Bihari log sirf ratta maarte hain" in the General thread. Can a moderator please take it down? It's not okay."
- **Clef's label:** TOXIC
- **Correct label:** ACCEPTABLE
- **WHY:** The comment is actually a reporting for a toxic comment but Clef classified as Toxic as it should have missed the gist of narration done by the user.

### Comment 40
- **Comment ID:** 40
- **Author:** Placement Cell CSE
- **Comment:** "Dear students, to register for the AI internship drive, verify your Moodle account at moodle-verify-cse.in with your username and password before Friday."
- **Clef's label:** acceptable
- **Correct label:** spam
- **Why:** This needs authentication check before passing comments for the classification. Meaning - if any link is given via authorized account then only it should be categorized as acceptable if any link is passed to comment then it should be classified as spam. But here we didn't introduce any gate and still clef classified this as acceptable.

### Comment 62
- **Comment ID:** 62
- **Author:** Prof. Sunita Rao
- **Comment:** "URGENT: free workshop on AI evaluation by an industry speaker this Saturday 11 AM, only 80 seats. Register before Thursday: forms.gle/cs307-eval-workshop. Attendance is optional."
- **Clef's label:** spam
- **Correct label:** acceptable
- **Why:** See again, had this person " Prof. Sunita Rao" gated or authorized before this comment should had to be acceptable but since we donot have clef classified as spam as it spams link for registration.

### Comment 91
- **Comment ID:** 91
- **Author:** Rohit Chawla
- **Comment:** "If anyone wants to tell Nikita what they think of her 'bias' report, she sits in the last row of lab 2 every Tuesday 😉"
- **Clef's label:** acceptable
- **Correct label:** toxic
- **Why:** This is doxxing and intimidation inviting confrontation against a student by revealing her specific physical seat and schedule in the lab. Clef missed the hostile intent because it lacked overt profanity.
