# Stage 1 Reflection: Human vs AI Software Development

Before using any AI tools the smartcare_v01 was using python lists, dictionaries and basic functions so that it could
store patient and practitioner appointment data. While using these functions for basic execution it also shows the limitations it had like lack of user input, schedule conflicts, and on validation for empty entries.

Using Microsoft Copilot as a tutor helped me analyse the code structure more in depth. it highlighted the key design issues, like how the appointment times were saved as text strings which were valid and empty practitioner names that could pass through unchecked. 

Copilot did make assumptions by providing a alternative version that was stripped down (`smartcare_ai.py`) that dropped error handling completely for simplicity.

To verify the AI's output, I executed `smartcare_ai,py` in PyCharm and checked for edge cases like empty strings. What shows was expected, the AI version accepted invalid data without any exceptions.

The main engineering work that remained for me was assesing the trade offs between human and and AI implementations, testing the code, and engineering a controlled improvement for the code to ensure robust input validation[cite:1].