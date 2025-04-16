import os

# Specify the environment variable you want to retrieve
env_var = "WG_PUBLIC_KEY"

# Get the value from the OpenVPN environment
value = os.environ.get(env_var, "NOT_SET")

# Define the output file path
output_file = "C:/Users/gr3ed/OneDrive/Documents/GitHub/OwlGuard_ZT-VPN/test/vpn_env.txt"

# Write the value to a file
with open(output_file, "w") as f:
    f.write(f"{env_var}={value}\n")

print(f"Saved {env_var} to {output_file}")
