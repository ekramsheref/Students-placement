---
icon: clipboard-list
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---
# Use Cases  

## **1.1: Processing Student Preferences for Department Specialization**  

#### **Actors**  
- **Administrator** – Responsible for uploading student preference data and managing the assignment process.  
- **Student** – Provides department preferences via an external form (Google Form or Microsoft Form).  

#### **Preconditions**  
- Students submit their department preferences through an external **Google Form or Microsoft Form**.  
- The **administrator collects** and compiles student preferences into an **Excel sheet with a standardized format** (including Student ID, Name, Preferences, GPA).  
- The system has **predefined eligibility criteria** for department assignment, including required subjects, GPA thresholds, and department capacity.  

#### **Main Success Scenario**  
1. The **administrator logs into the system**.  
2. The **administrator uploads the Excel sheet** containing student preferences.  
3. The system **validates the file structure and data integrity** (e.g., checks for missing fields, correct format).  
4. The system **applies department eligibility criteria**, filtering students based on required subjects, GPA, and available capacity.  
5. The system **automatically assigns students to departments** based on their preferences and eligibility.  
6. The system **generates an output file** (Excel format) listing students and their assigned departments.  
7. The administrator **downloads the output file** for further use.  

#### **Alternative Scenarios**  

##### **A1. Invalid or Corrupted Data File**  
- 3a. The system detects an **incorrect format, missing fields, or corrupted data**.  
- 3b. The system **notifies the administrator** and requests a valid file.  
- 3c. **Use case ends**.  

##### **A2. System Error During Processing**  
- 4a. The system encounters an **error while applying eligibility criteria or processing assignments**.  
- 4b. The system **logs the error and notifies the administrator**.  
- 4c. **Use case ends**.  

##### **A3. Student Does Not Meet Any Department’s Criteria**  
- 5a. The system identifies students **who do not qualify for any department**.  
- 5b. The system assigns them to a **general category** or flags them for **manual review**.  
- 5c. The administrator manually reviews and resolves assignments.

---  

## **1.2: Adding a New Program to the System**  

#### **Actors**  
- **System Administrator** – Responsible for managing academic programs in the system.  

#### **Preconditions**  
- The administrator has access to the application with **administrative privileges**.  

#### **Main Success Scenario**  
1. The **administrator logs into the application**.  
2. The **administrator navigates to the "Manage Programs" section**.  
3. The **administrator selects the option to add a new program**.  
4. The system **prompts the administrator to enter details** for the new program (e.g., name, eligibility criteria, capacity).  
5. The administrator **enters the required information and submits the form**.  
6. The system **saves the new program and updates the list** of available programs.  
7. The system **confirms the successful addition** of the new program to the administrator.  

#### **Alternative Scenarios**  

##### **A1. Missing or Incomplete Information**  
- 5a. The system detects **missing or incomplete information** in the form.  
- 5b. The system **prompts the administrator** to complete all required fields.  
- 5c. **Use case resumes at step 5**.  

##### **A2. System Error During Program Addition**  
- 6a. The system encounters an **error while saving the new program**.  
- 6b. The system **logs the error and notifies the administrator**.  
- 6c. **Use case ends**.  

---  

## **1.3: Updating Eligibility Criteria for Existing Programs**  

#### **Actors**  
- **System Administrator** – Responsible for modifying program eligibility requirements.  

#### **Preconditions**  
- The administrator has access to the application with **administrative privileges**.  
- **Existing programs are already defined** in the system.  

#### **Main Success Scenario**  
1. The **administrator logs into the application**.  
2. The **administrator navigates to the "Manage Programs" section**.  
3. The **administrator selects an existing program** to update.  
4. The system **displays the current eligibility criteria** for the selected program.  
5. The administrator **modifies the criteria** (e.g., subjects, GPA, capacity) as needed.  
6. The administrator **submits the changes**.  
7. The system **saves the updated criteria and confirms the changes** to the administrator.  

#### **Alternative Scenarios**  

##### **A1. Invalid Criteria Input**  
- 5a. The system detects **invalid input** for the criteria.  
- 5b. The system **prompts the administrator** to correct the input.  
- 5c. **Use case resumes at step 5**.  

---  

## **1.4: Deleting an Existing Programs**  

#### **Actors**  
- **System Administrator** – Responsible for removing academic programs from the system.  

#### **Preconditions**  
- The **system administrator has access** to the application with the necessary privileges.  
- The **program to be deleted exists** in the system.  

#### **Main Success Scenario**  
1. The **system administrator logs into the application**.  
2. The administrator **navigates to the "Manage Programs" section**.  
3. The administrator **searches for the program** to be deleted.  
4. The system **displays the details** of the selected program.  
5. The administrator **selects the option to delete the program**.  
6. The system **prompts the administrator to confirm** the deletion.  
7. The administrator **confirms the deletion**.  
8. The system **deletes the program and updates the list** of available programs.  
9. The system **confirms the successful deletion** to the administrator.  

#### **Alternative Scenarios**  

##### **A1. Program Not Found**  
- 3a. The system cannot **find the program** based on the provided information.  
- 3b. The system **notifies the administrator** and suggests verifying the program details.  
- 3c. **Use case ends**.  

##### **A2. Deletion Confirmation Denied**  
- 6a. The administrator **cancels the deletion process**.  
- 6b. The system **returns to the program details view**.  
- 6c. **Use case ends**.  

##### **A3. System Error During Deletion**  
- 8a. The system encounters an **error while deleting the program**.  
- 8b. The system **logs the error and notifies the administrator**.  
- 8c. **Use case ends**.  

#### **Postconditions**  
- The **program is removed from the system**.  
- The **changes are reflected** in any subsequent processing or reports.

---  

## **1.5: User Access Management**  

#### **Actors**  
- **System Administrator** – Manages user access and permissions.  

#### **Preconditions**  
- The system has multiple users with varying access needs.  

#### **Main Success Scenario**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "User Management" section**.  
3. The **administrator selects the option to add or modify user access**.  
4. The system **displays a list of current users and their access levels**.  
5. The administrator **selects a user to modify or adds a new user**.  
6. The administrator **assigns or updates the user's access level and permissions**.  
7. The administrator **submits the changes**.  
8. The system **saves the changes and confirms successful completion**.  

#### **Alternative Scenarios**  

##### **A1. Invalid User Information**  
- 6a. The system detects **invalid user information**.  
- 6b. The system **prompts the administrator** to correct the information.  
- 6c. **Use case resumes at step 6**.  

---

## **1.6: Generating Reports for Department Allocation**  

#### **Actors**  
- **Administrator** – Generates reports for student assignments.  
- **Department Head** – Receives and reviews the reports.  

#### **Preconditions**  
- The system has **processed student preferences** and assigned them to departments.  

#### **Main Success Scenario**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "Reports" section**.  
3. The **administrator selects the option to generate a department allocation report**.  
4. The system **compiles data on student assignments**, including:  
   - Number of students per department.  
   - Average GPA.  
   - Unmet preferences.  
5. The system **generates a detailed report** in the chosen format (e.g., PDF, Excel).  
6. The administrator **downloads the report** for distribution.  

#### **Alternative Scenarios**  

##### **A1. No Data Available**  
- 4a. The system detects that **no data is available** for report generation.  
- 4b. The system **notifies the administrator** and suggests checking data processing status.  
- 4c. **Use case ends**.  

---

## **1.7: Sending Notifications to Department Heads**  

#### **Actors**  
- **Administrator** – Sends notifications regarding student assignments.  
- **Department Head** – Receives the notifications.  

#### **Preconditions**  
- The system has **processed student preferences** and assigned them to departments.  

#### **Main Success Scenario**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "Notifications" section**.  
3. The **administrator selects the option to send notifications to department heads**.  
4. The system **generates notifications with student assignment details and statistics**.  
5. The system **sends notifications via email** to department heads.  
6. The system **confirms successful delivery** to the administrator.  

#### **Alternative Scenarios**  

##### **A1. Notification Delivery Failure**  
- 5a. The system encounters an **error while sending notifications**.  
- 5b. The system **logs the error and notifies the administrator**.  
- 5c. **Use case ends**.  

---  

## **1.8: Sending Notifications to Students**  

#### **Actors**  
- **Administrator** – Sends notifications.  
- **Student** – Receives notifications.  

#### **Preconditions**  
- The system has **processed student preferences** and assigned them to departments.  
- Students have **registered their academic email addresses** in the system.  

#### **Main Success Scenario**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "Notifications" section**.  
3. The **administrator selects the option to send notifications to students**.  
4. The system **automatically generates notifications** with department assignment details.  
5. The system **sends notifications via email** to students.  
6. The system **confirms successful delivery** to the administrator.  

#### **Alternative Scenarios**  

##### **A1. Notification Delivery Failure**  
- 5a. The system encounters an **error while sending notifications**.  
- 5b. The system **logs the error and notifies the administrator**.  
- 5c. **Use case ends**.  

---

## **1.9: Updating Student Preferences**  

#### **Actors**  
- **Administrator** – Updates student preferences.  

#### **Preconditions**  
- The **student has already submitted their initial preferences**.  
- The **administrator has the necessary privileges** to update student preferences.  

#### **Main Success Scenario**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "Student Preferences" section**.  
3. The **administrator searches for the student by name or ID**.  
4. The system **displays the student's current preferences**.  
5. The **administrator selects the option to edit the preferences**.  
6. The **administrator updates the preferences** as requested.  
7. The **administrator submits the changes**.  
8. The system **saves the updated preferences and confirms the changes**.  

#### **Alternative Scenarios**  

##### **A1. Student Not Found**  
- 3a. The system **cannot find the student** based on the provided information.  
- 3b. The system **notifies the administrator** and suggests verifying details.  
- 3c. **Use case ends**.  

##### **A2. Invalid Preference Input**  
- 6a. The system detects **invalid input** for the preferences.  
- 6b. The system **prompts the administrator** to correct the input.  
- 6c. **Use case resumes at step 6**.  

##### **A3. System Error During Update**  
- 8a. The system **encounters an error** while saving the preferences.  
- 8b. The system **logs the error and notifies the administrator**.  
- 8c. **Use case ends**.  

#### **Postconditions**  
- The student's **preferences are updated** in the system.  
- The changes are **reflected in subsequent processing and reports**.  

---

## **1.10: Data Backup and Recovery**  

#### **Actors**  
- **Administrator** – Manages data backup and recovery.  

#### **Preconditions**  
- The system is **operational** and contains **data that needs to be backed up**.  

#### **Main Success Scenario: Backup Process**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "Data Management" section**.  
3. The **administrator selects the option to perform a data backup**.  
4. The system **compiles all relevant data** into a backup file.  
5. The system **prompts the administrator** to choose a storage location.  
6. The **administrator selects a location** and confirms the backup.  
7. The system **saves the backup file** and confirms successful completion.  

#### **Main Success Scenario: Recovery Process**  
1. The **administrator logs into the system**.  
2. The **administrator navigates to the "Data Management" section**.  
3. The **administrator selects the option to restore data from a backup**.  
4. The system **prompts the administrator** to select a backup file.  
5. The **administrator selects the backup file** and confirms the restoration.  
6. The system **restores the data** and confirms successful completion.  

#### **Alternative Scenarios**  

##### **A1. Backup Process Error**  
- 4a. The system **encounters an error** during the backup process.  
- 4b. The system **logs the error and notifies the administrator**.  
- 4c. **Use case ends**.  

