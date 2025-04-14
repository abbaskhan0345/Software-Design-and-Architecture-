🎯 Objective:
Use the Decorator Design Pattern to dynamically add features to a basic Coffee order in a coffee shop system — like adding milk, sugar, whipped cream, etc., to the base coffee without modifying the original class.

✅ Real-World Problem Scenario:
Imagine a coffee shop where customers can order a basic coffee, but they can also customize it with add-ons like:

Milk 🥛

Sugar 🍬

Whipped Cream 🍦

Caramel 🍯

Each of these add-ons increases the cost of the coffee and may change its description.

🧱 Decorator Pattern Structure:
Component Interface – defines the interface for objects that can have responsibilities added to them.

Concrete Component – defines an object to which additional responsibilities can be attached.

Decorator – maintains a reference to a component object and defines an interface that conforms to the component’s interface.

Concrete Decorators – add responsibilities to the component.
