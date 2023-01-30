from .mongodb import collection


class MongoPipeline(object):

    def process_item(self,item,spider):

        data={

            "wine_id": item["wine_id"],
            "name_k" : item["name_k"],
            "name_e" : item["name_e"],
            "detail" : item["detail"],
            "taste" : item["taste"],
            "information" : item["information"],
            "awards" : item["awards"],
            "image" : item["image"],

        }

        collection.insert(data)
             
        return item
