export const validatePlan = (plan) => {
    return plan["Breakfast"] && plan["Lunch"] && plan["Dinner"]
}