# test_jwt.py
import jwt

secret = "a3f8c2e1b4d7e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8f9a0b1c2d3e4"

token = jwt.encode({"user": "test"}, key=secret, algorithm="HS256")
print(f"PyJWT version: {jwt.__version__}")
print(f"Encoded token: {token}")

decoded = jwt.decode(token, key=secret, algorithms=["HS256"])
print(f"Decoded: {decoded}")
