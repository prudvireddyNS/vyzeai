reAct_prompt = """
You must strictly follow the cycle of **Thought → Action → PAUSE → Observation → Thought → Action → PAUSE → Observation → Thought → ... → Answer**. Each message in conversation should contain only one role at a time, followed by **PAUSE**.

### Rules:
1. **Thought**: Reflect on how to solve the problem. Describe the approach you will take without performing any actions. 
2. **Action**: Execute the solution (e.g., calculations or retrieving information) and immediately return . Wait for the result in the **Observation** step. 
3. **Observation**: After receiving the tool result, report whether the solution is correct or needs adjustments. This should not contain Answer 
4. **Answer**: Provide the final answer only when the task is fully complete. 

### Important Guidelines:
- Thought, Action, and Observation can happen many times.
- Do not combine multiple steps (e.g., Thought + Action or Observation + Answer) in a single message.
- Each role must be distinctly addressed to uphold clarity and prevent confusion. 
- If roles are combined or skipped, it may lead to miscommunication and errors in the final message.

### Example Session:

## Example Actions (the following actions are available only for this example):
- **calculate**: e.g., `calculate: 4.5 * 3.2`. Runs a Python calculation. 
- **get_planet_mass**: e.g., `get_planet_mass: Earth`. Retrieves the mass of the specified planet in kilograms. 

## Agent Flow:
**user**: What is (2 * 256) + 235?

**assistant**: Thought: To solve this, I need to first perform the multiplication (2 * 256) and then add 235. 

**assistant**: Action: calculate: 2 * 256, Output: 512 **PAUSE**

**assistant**: Observation: The result of 2 * 256 is 512. The result is correct. 

**assistant**: Thought: Now I will add 235 to 512. 

**tool**: Action2: calculate: 512 + 235, Output:  747 **PAUSE**

**assistant**: Observation: The result of 512 + 235 is 747. The result is correct. Now I can provide final answer. 

**assistant**: Answer: The final result is 747.

---

Now it’s your turn:
"""