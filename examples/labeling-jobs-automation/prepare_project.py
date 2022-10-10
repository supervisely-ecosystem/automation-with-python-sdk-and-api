# See spatial labels and image and object tags sections
# for more info about creating object classes and tags
# on developer portal

import supervisely as sly

def prepare_project(api, id):
    # download project meta
    project_meta_json = api.project.get_meta(id)
    project_meta = sly.ProjectMeta.from_json(project_meta_json)
    
    # create TagMetas
    size_tag_meta = sly.TagMeta(
        name="size",
        value_type=sly.TagValueType.ONEOF_STRING,
        color=[189, 16, 224],
        possible_values=["small", "medium", "large"],
        applicable_to=sly.TagApplicableTo.OBJECTS_ONLY,
        applicable_classes=["lemon", "kiwi"]
    )
    
    origin_tag_meta = sly.TagMeta(
        name="origin", 
        value_type=sly.TagValueType.ANY_STRING,
        color=[139, 87, 42],
        applicable_to=sly.TagApplicableTo.OBJECTS_ONLY,
        applicable_classes=["lemon", "kiwi"]
    )
    
    # add TagMetas to project meta
    tag_metas = [size_tag_meta, origin_tag_meta]
    for tag_meta in tag_metas:
        if tag_meta not in project_meta.tag_metas:
            project_meta = project_meta.add_tag_meta(new_tag_meta=tag_meta)
              
    # Create ObjClasses
    lemon_obj_class = sly.ObjClass(
        name="lemon", 
        geometry_type=sly.Bitmap, 
        color=[80, 227, 194]
        )
    kiwi_obj_class = sly.ObjClass(
        name="kiwi", 
        geometry_type=sly.Bitmap, 
        color=[208, 2, 27]
        )
    
    # add ObjClasses to project meta
    obj_classes = [lemon_obj_class, kiwi_obj_class]
    for obj_class in obj_classes:
        if obj_class not in project_meta.obj_classes:
            project_meta = project_meta.add_obj_class(new_obj_class=obj_class)
    
    # update project meta
    api.project.update_meta(id=id, meta=project_meta)