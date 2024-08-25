from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    height = models.PositiveIntegerField(null=True, blank=True, help_text="Height in cm")
    weight = models.PositiveIntegerField(null=True, blank=True, help_text="Weight in kg")
    age = models.PositiveIntegerField(null=True, blank=True, help_text="Age in years")
    weight_goal = models.PositiveIntegerField(null=True, blank=True, help_text="Weight Goal in kg")
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), default='female')
    def __str__(self):
        return self.username
    def calculate_bmr(self):
        """Calculate BMR (Basal Metabolic Rate) based on user's details."""
        if self.gender == 'male':
            # BMR formula for men
            bmr = 66 + (13.7 * self.weight) + (5 * self.height) - (6.8 * self.age)
        else:
            # BMR formula for women
            bmr = 655 + (9.6 * self.weight) + (1.8 * self.height) - (4.7 * self.age)
        
        return round(bmr, 2)
    def calculate_bmi(self):
        """Calculate BMI (Body Mass Index) based on user's height and weight."""
        if self.height and self.weight:
            # Convert height from cm to meters
            height_m = self.height / 100
            # BMI formula
            bmi = self.weight / (height_m ** 2)
            return round(bmi, 2)
        return None
    
    def get_health_status(self):
        """Determine health status based on BMI."""
        bmi = self.calculate_bmi()
        if bmi is None:
            return "BMI not available"
        elif bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal Weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def recommended_calorie_intake(self):
        """Calculate recommended calorie intake based on BMR and weight goal."""
        bmr = self.calculate_bmr()
        if bmr is None:
            return "BMR not available"
        
        if self.weight_goal is None:
            return round(bmr, 2)
        
        # Simple approach for calorie adjustment:
        # - To maintain weight: BMR
        # - To lose weight: BMR - 500 kcal/day (approximate)
        # - To gain weight: BMR + 500 kcal/day (approximate)
        if self.weight_goal < self.weight:
            calorie_intake = bmr - 500  # To lose weight
        elif self.weight_goal > self.weight:
            calorie_intake = bmr + 500  # To gain weight
        else:
            calorie_intake = bmr  # To maintain weight

        return round(calorie_intake, 2)
    def overweight_amount(self):
        """Calculate how much weight user is overweight."""
        bmi = self.calculate_bmi()
        if bmi is None:
            return "BMI not available"
        
        height_m = self.height / 100 if self.height else None
        if height_m is None:
            return "Height not available"
        
        # Calculate ideal weight range for normal BMI (18.5 - 24.9)
        ideal_min_weight = 18.5 * (height_m ** 2)
        ideal_max_weight = 24.9 * (height_m ** 2)
        
        if self.weight is None:
            return "Weight not available"
        
        if self.weight <= ideal_max_weight:
            return "You are not overweight"
        
        excess_weight = self.weight - ideal_max_weight
        return round(excess_weight, 2)
    
    def days_to_reach_goal(self):
        """Calculate the number of days required to reach the weight goal."""
        if self.weight_goal is None or self.weight is None:
            return "Weight or weight goal not available"
        
        # Calculate the weight difference
        weight_difference = self.weight - self.weight_goal
        if weight_difference <= 0:
            return "Weight goal already achieved or not set"

        # Calculate calorie deficit or surplus
        calorie_intake = self.recommended_calorie_intake()
        if isinstance(calorie_intake, str):
            return calorie_intake
        
        # Assuming a daily caloric deficit of 500 kcal results in approximately 0.5 kg weight loss per week
        kcal_per_kg = 7700  # Approximate number of calories required to lose or gain 1 kg
        weekly_weight_change = 0.5  # Weight change per week in kg
        daily_calorie_deficit = 500  # Caloric deficit per day
        
        # Calculate weight change per day
        weight_change_per_day = daily_calorie_deficit / kcal_per_kg
        
        # Calculate the number of days required
        days_required = weight_difference / weight_change_per_day
        
        return round(days_required, 2)
    
class FoodLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='food_logs')
    food_name = models.CharField(max_length=255)
    calories = models.PositiveIntegerField(help_text="Calories in the portion")
    date_logged = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.calories} kcal (Logged by {self.user.username} on {self.date_logged})"