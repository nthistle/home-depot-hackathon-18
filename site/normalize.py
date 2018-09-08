cols = ['left_eye_center_x',
 'left_eye_center_y',
 'right_eye_center_x',
 'right_eye_center_y',
 'left_eye_inner_corner_x',
 'left_eye_inner_corner_y',
 'left_eye_outer_corner_x',
 'left_eye_outer_corner_y',
 'right_eye_inner_corner_x',
 'right_eye_inner_corner_y',
 'right_eye_outer_corner_x',
 'right_eye_outer_corner_y',
 'left_eyebrow_inner_end_x',
 'left_eyebrow_inner_end_y',
 'left_eyebrow_outer_end_x',
 'left_eyebrow_outer_end_y',
 'right_eyebrow_inner_end_x',
 'right_eyebrow_inner_end_y',
 'right_eyebrow_outer_end_x',
 'right_eyebrow_outer_end_y',
 'nose_tip_x',
 'nose_tip_y',
 'mouth_left_corner_x',
 'mouth_left_corner_y',
 'mouth_right_corner_x',
 'mouth_right_corner_y',
 'mouth_center_top_lip_x',
 'mouth_center_top_lip_y',
 'mouth_center_bottom_lip_x',
 'mouth_center_bottom_lip_y',
 'Image']
FEAT_DICT = {i:"_".join(cols[i].split("_")[:-1]) for i in range(len(cols)-1) if i % 2 == 1}

import math

def find_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_mid(p1, p2):
    return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)

def scale(factor, p1, p2):
    mid = find_mid(p1, p2)
    new_p1 = (int(factor * (p1[0] - mid[0]) + mid[0]), int(factor * (p1[1] - mid[1]) + mid[1]))
    new_p2 = (int(factor * (p2[0] - mid[0]) + mid[0]), int(factor * (p2[1] - mid[1]) + mid[1]))
    return (new_p1, new_p2)


def find_factor(orig_feat_point, our_feat_point):
    dist_orig = find_distance(orig_feat_point[0], orig_feat_point[1])
    dist_our = find_distance(our_feat_point[0], our_feat_point[1])
    return dist_orig / dist_our

def scale_all_feats(factor, our_features):
    new_features = []
    for i in range(10):
        if i % 2 == 1:
            continue
        left_name = our_features[i][0]
        right_name = our_features[i + 1][0]
        left = our_features[i]
        right = our_features[i + 1]
        scaled_feats = scale(factor, left[1], right[1])
        this_left_feat = (left_name, scaled_feats[0])
        this_right_feat = (right_name, scaled_feats[1])
        new_features.append(this_left_feat)
        new_features.append(this_right_feat)
    new_features.append(our_features[10])
    for i in range(11, len(our_features)-1):
        if i % 2 == 0:
            continue
        left_name = our_features[i][0]
        right_name = our_features[i + 1][0]
        left = our_features[i]
        right = our_features[i + 1]
        scaled_feats = scale(factor, left[1], right[1])
        this_left_feat = (left_name, scaled_feats[0])
        this_right_feat = (right_name, scaled_feats[1])
        new_features.append(this_left_feat)
        new_features.append(this_right_feat)
    
    return new_features



def make_feature_list(img_data, FEAT_DICT=FEAT_DICT):
    these_features = []
    for i in range(15):
        x = int(img_data[2*i])
        y = int(img_data[2*i+1])
        these_features.append((FEAT_DICT[2*i + 1], (x, y)))
    return these_features


def find_and_scale(orig_features, our_features):
    orig_mouth = [x[1] for x in orig_features if "eye_outer_corner" in x[0]]
    our_mouth = [x[1] for x in our_features if "eye_outer_corner" in x[0]]
    factor = find_factor(orig_mouth, our_mouth)
    return scale_all_feats(factor, our_features)



def compare_mouth_width(orig_features, our_features):
    orig_mouth = [x[1] for x in orig_features if "mouth" in x[0] and "corner" in x[0]]
    orig_dist = find_distance(orig_mouth[0], orig_mouth[1])
    our_mouth = [x[1] for x in our_features if "mouth" in x[0] and "corner" in x[0]]
    our_dist = find_distance(our_mouth[0], our_mouth[1])
    dist = abs(orig_dist - our_dist)
    return 1 - (dist / orig_dist)



def compare_mouth_height(orig_features, our_features):
    orig_mouth = [x[1] for x in orig_features if "mouth" in x[0] and "center" in x[0]]
    orig_dist = find_distance(orig_mouth[0], orig_mouth[1])
    our_mouth = [x[1] for x in our_features if "mouth" in x[0] and "center" in x[0]]
    our_dist = find_distance(our_mouth[0], our_mouth[1])
    dist = abs(orig_dist - our_dist)
    return 1 - (dist / orig_dist)



def compare_left_eyebrow(orig_features, our_features):
    orig_eyebrow = [x[1] for x in orig_features if "eyebrow" in x[0] and "left" in x[0]] # get inner and outer end of eyebrow
    orig_mid_eyebrow = find_mid(orig_eyebrow[0], orig_eyebrow[1]) #get midpoint between the two
    orig_center_eye = [x[1] for x in orig_features if "left_eye_center" in x[0]] # get coordinates for center of left eye
    orig_dist = find_distance(orig_mid_eyebrow, orig_center_eye[0]) #find distance between mid eyebrow and center of eye
    our_eyebrow = [x[1] for x in our_features if "eyebrow" in x[0] and "left" in x[0]]
    our_mid_eyebrow = find_mid(our_eyebrow[0], our_eyebrow[1])
    our_center_eye = [x[1] for x in our_features if "left_eye_center" in x[0]]
    our_dist = find_distance(our_mid_eyebrow, our_center_eye[0])
    dist = abs(orig_dist - our_dist)
    return 1 - (dist / orig_dist)



def compare_right_eyebrow(orig_features, our_features):
    orig_eyebrow = [x[1] for x in orig_features if "eyebrow" in x[0] and "right" in x[0]]
    orig_mid_eyebrow = find_mid(orig_eyebrow[0], orig_eyebrow[1])
    orig_center_eye = [x[1] for x in orig_features if "right_eye_center" in x[0]]
    orig_dist = find_distance(orig_mid_eyebrow, orig_center_eye[0])
    our_eyebrow = [x[1] for x in our_features if "eyebrow" in x[0] and "right" in x[0]]
    our_mid_eyebrow = find_mid(our_eyebrow[0], our_eyebrow[1])
    our_center_eye = [x[1] for x in our_features if "right_eye_center" in x[0]]
    our_dist = find_distance(our_mid_eyebrow, our_center_eye[0])
    dist = abs(orig_dist - our_dist)
    return 1 - (dist / orig_dist)



def compare_all_feats(orig_features, our_features):
    mw = compare_mouth_width(orig_features, our_features)
    mh = compare_mouth_height(orig_features, our_features)
    le = compare_left_eyebrow(orig_features, our_features)
    re = compare_right_eyebrow(orig_features, our_features)
    avg = (mw + mh + le + re) / 4.0
    return (abs(avg)**2, abs(mw), abs(mh), abs(le), abs(re))



def data_to_features(orig_data, our_data):
    orig_features = make_feature_list(orig_data)
    our_features = make_feature_list(our_data)
    return (orig_features, our_features)



def data_to_conclusion(orig_data, our_data):
    orig_features, our_features = data_to_features(orig_data, our_data)
    our_features = find_and_scale(orig_features, our_features)
    return compare_all_feats(orig_features, our_features)

