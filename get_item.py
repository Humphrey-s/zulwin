import requests as r
from models.item import Item
from datetime import datetime
from uuid import uuid4
import os

if __name__ == "__main__":
	p = r.get("https://fakestoreapi.com/products")

	if p.status_code == 200:
		print("product in process\n")
		data = p.json()
		for i in data:
			i["seller_id"] = "28154b37-f515-49ef-bbbc-42b87ebc8fc6"
			i.pop("id")
			i.pop("rating")
			img = r.get(i["image"])
			if img.status_code == 200:
				current_path = os.getcwd()
				folder_path = "web_dynamic\\static\\assets\\public\\"
				full_path = os.path.join(current_path, folder_path)
				name = f"{str(uuid4())}.{datetime.now().strftime('%Y-%m-%d')}{i['image'][-4:]}"
				file_path = os.path.join(full_path, name)
				i["image"] = name
				i["name"] = i["title"]
				i["expiry_date"] = "2025-11-09"
				with open(file_path, "wb+") as f:
					f.write(img.content)

				print(f"{name}\n")
				instance = Item(**i)
				instance.save()



