from cl_client import cl_get

o = cl_get("opinions/4289306/").json()

for name in ["plain_text", "html", "html_lawbox", "html_columbia",
             "html_anon_2020", "xml_harvard", "html_with_citations"]:
    print(name, len(o.get(name) or ""))

print("download_url:", o.get("download_url"))
print("local_path:", o.get("local_path"))
print("page_count:", o.get("page_count"))