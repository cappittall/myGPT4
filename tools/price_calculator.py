class CoatingPriceCalculator:
    def __init__(self, df):
        self.df = df
        self.coating_types = {
            1: "BALINIT® A (TiN)",
            2: "BALINIT® B (TiCN)",
            3: "BALINIT® C (WC/C)",
            4: "BALINIT® CAST (CrC)",
            5: "BALINIT® D (CrN)",
            6: "BALINIT® FUTURA NANO (TiAlN)",
            7: "BALINIT® FUTURA TOP (TiAlN)",
            8: "BALINIT® A + C",
            9: "BALINIT® B + C",
            10: "BALINIT® FUTURA NANO + C",
            11: "BALINIT® G + C",
            12: "BALINIT® TRITON (DLC)",
            13: "BALINIT® LUMENA (TiAlN)",
            14: "BALINIT® ALCRONA (AlCrN)"
        }

    def calculate_coating_price(self, piece_type, diameter=None, length=None, width=None, height=None, type = 1):
        if piece_type == "cylinder":
            return self._calculate_cylinder_price(diameter, height, type)
        elif piece_type == "quadrangular":
            return self._calculate_quadrangular_price(length, width, height)
        else:
            raise ValueError("Invalid piece type. Supported types: 'cylinder', 'quadrangular'.")

    def _calculate_cylinder_price(self, diameter, height, type):
        mass = (diameter / 2) ** 2 * 3.14 * height / 1000

        ind = self._find_matching_coating_index(mass)
        row_price = self.df.at[ind, "I"] * mass

        if type == 14:
            o5 = row_price * 1.4
        else:
            o5 = row_price

        if type == 1:
            return row_price * 0.67
        elif ind in [7, 8, 9, 10, 11, 12, 13]:
            return row_price * 1.6
        else:
            return o5

    def _calculate_quadrangular_price(self, length, width, height):
        m6 = length * width * height / 1000

        k5 = self._find_matching_coating_index(length)
        l11 = self.df.at[k5, "I"] * self.df.at[k5, "C"]

        if k5 == 14:
            l14 = l11 * 1.4
        else:
            l14 = l11

        if k5 == 1:
            return l11 * 0.67
        elif k5 in [7, 8, 9, 10, 11, 12, 13]:
            return l11 * 1.6
        else:
            return l14

    def _find_matching_coating_index(self, mass):
        for index, row in self.df.iterrows():
            if mass <= row["H"]:
                print( ' dimension <= row["H"] ', mass, index,'>>', row['H'])
                return index

        raise ValueError("Matching coating index not found for the given dimension.")




import pandas as pd

# Create the DataFrame
data = {
    "H": [0.100, 0.200, 0.300, 0.400, 0.500, 0.600, 0.800, 1.000, 2.000, 3.000, 4.000, 6.000, 10.000, 15.000, 20.000, 30.000, 45.000, 60.000, 75.000, 120.000, 140.000, 240.000, 700.000, 1200.000, 1800.000, 3500.000, 4500.000, 5500.000, 7500.000, 8500.000, 9500.000, 25000.000, 65000.000, 85000.000],
    "I": [10.58, 8.81, 4.41, 3.35, 2.65, 2.30, 1.95, 1.67, 1.33, 1.12, 0.83, 0.63, 0.44, 0.34, 0.30, 0.23, 0.20, 0.19, 0.18, 0.17, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03],
    "J": ["BALINIT® A (TiN)", "BALINIT® B (TiCN)", "BALINIT® C (WC/C)", "BALINIT® CAST (CrC)", "BALINIT® D (CrN)", "BALINIT® FUTURA NANO (TiAlN)", "BALINIT® FUTURA TOP (TiAlN)", "BALINIT® A + C", "BALINIT® B + C", "BALINIT® FUTURA NANO + C", "BALINIT® G + C", "BALINIT® TRITON (DLC)", "BALINIT® LUMENA (TiAlN)", "BALINIT® ALCRONA (AlCrN)", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    "C": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0],
}

df = pd.DataFrame(data, index=range(5, len(data["H"]) + 5))

# Create the CoatingPriceCalculator instance
calculator = CoatingPriceCalculator(df)

# Calculate the coating price for a cylinder
cylinder_price = calculator.calculate_coating_price("cylinder", diameter=100, height=200, type=13)
print("Cylinder Price:", cylinder_price)

# Calculate the coating price for a quadrangular piece
""" quadrangular_price = calculator.calculate_coating_price("quadrangular", length=150, width=100, height=50)
print("Quadrangular Price:", quadrangular_price) """
