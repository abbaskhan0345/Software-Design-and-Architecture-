from abc import ABC, abstractmethod

# Component
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass

    @abstractmethod
    def description(self):
        pass

# Concrete Component
class BasicCoffee(Coffee):
    def cost(self):
        return 5

    def description(self):
        return "Basic Coffee"

# Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost()

    def description(self):
        return self._coffee.description()

# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 1.5

    def description(self):
        return self._coffee.description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.5

    def description(self):
        return self._coffee.description() + ", Sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 2.0

    def description(self):
        return self._coffee.description() + ", Whipped Cream"

# Client Code
def main():
    order = BasicCoffee()
    print(f"{order.description()} = ${order.cost()}")

    # Add milk
    order = MilkDecorator(order)
    # Add sugar
    order = SugarDecorator(order)
    # Add whipped cream
    order = WhippedCreamDecorator(order)

    print(f"{order.description()} = ${order.cost()}")

if __name__ == "__main__":
    main()

#Basic Coffee = $5
#Basic Coffee, Milk, Sugar, Whipped Cream = $9.0
