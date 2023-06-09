import csv

import numpy

from new_methods.apriori.tools import generate_apriori
from new_methods.expr.train import device
from new_methods.data.airplane_data import *
from CAM_tools import *
import os
from PIL import Image
import cv2
import pickle
from new_methods.utils.visualise import show

# bbox_list_name = ['bbox_pre3', 'bbox_pre4', 'bbox_pre3a', 'bbox_pre4a', 'bbox_pre34', 'bbox_pre3a4a', 'bbox_pre33a',
#                   'bbox_pre34a',
#                   'bbox_pre33a4a', 'bbox_pre43a', 'bbox_pre3a4', 'bbox_pre44a', 'bbox_pre43a4a', 'bbox_pre3a4a4',
#                   'bbox_pre3a34', 'bbox_pre4a34', 'bbox_pre344a', 'bbox_pre343a4a']
#
# folder = ['\\3\\', '\\4\\', '\\3a\\', '\\4a\\', '\\34\\', '\\3a4a\\', '\\33a\\', '\\34a\\', '\\33a4a\\', '\\43a\\',
#           '\\3a4\\', '\\44a\\', '\\43a4a\\', '\\3a4a4\\'
#     , '\\3a34\\', '\\4a34\\', '\\344a\\', '\\343a4a\\']

bbox_list_name = ['bbox_pre3', 'bbox_pre4', 'bbox_pre34']

folder = ['\\3\\', '\\4\\', '\\34\\']


def test(model, store_path, box_file, gt_file):
    model.to(device)
    model.eval()

    # load data
    test_data_size = 0
    corrects = 0.0
    str = r'D:\CODE_AND_RESULTS\data\test_airplane'
    # folder = ['\\3\\', '\\4\\', '\\3a\\', '\\4a\\', '\\34\\', '\\3a4a\\', '\\33a\\', '\\34a\\', '\\33a4a\\', '\\43a\\',
    #           '\\3a4\\', '\\44a\\', '\\43a4a\\', '\\3a4a4\\'
    #     , '\\3a34\\', '\\4a34\\', '\\344a\\', '\\343a4a\\']
    folder = ['\\3\\', '\\4\\', '\\34\\']

    TP = [0.0] * 3
    FP = [0.0] * 3
    FN = [0.0] * 3
    # preBBox_num = 0
    # BBox_num = 0

    for img in os.listdir(str + '/img'):
        # for img in os.listdir(str + ):
        # inputs

        image = Image.open(str + '/img/' + img)
        # image = Image.open(str + '\\train\\positive img/' + img)
        inputs = test_data_transform(image)
        inputs = inputs.unsqueeze(0)
        inputs = inputs.to(device)

        # outputs
        outputs = model(inputs)
        confidence, preds = torch.max(outputs, 1)

        layer_map3, layer_map4 = model.get_salience_maps()
        cam3 = generateCAM(str + '/img/' + img, layer_map3, store_path, None)
        cam4 = generateCAM(str + '/img/' + img, layer_map4, store_path, preds)

        ##cam3a = generate_apriori(str + '/img/' + img, layer_map3, os.path.join(store_path, 'scam'), minimum_support=.4)
        ##cam4a = generate_apriori(str + '/img/' + img, model.get_dcam(), os.path.join(store_path, 'dcam'),
        #                         minimum_support=.6)


        # print(cam3a)
        # cv2.imshow('image',cam3)
        # cv2.waitKey(0)
        # print(cam4)
        # cv2.imshow('image', cam4)
        # cv2.waitKey(0)
        bbox_pre3 = generateBBox(cam3, confidence.item(), True)
        bbox_pre4 = generateBBox(cam4, confidence.item(), True)
        ##bbox_pre3a = generateBBox(cam3a, 1, False)
        ##bbox_pre4a = generateBBox(cam4a, 1, False)
        # print('bbox_pre3')
        # for obj in bbox_pre3:
        #     print(obj.__str__())
        # print('bbox_pre4')
        # for obj in bbox_pre4:
        #     print(obj.__str__())
        # print('bbox_pre3a')
        # for obj in bbox_pre3a:
        #     print(obj.__str__())
        # print('bbox_pre4a')
        # for obj in bbox_pre4a:
        #     print(obj.__str__())
        # print(bbox_pre3)
        # print(bbox_pre4)
        # print(bbox_pre3a)
        # print(bbox_pre4a)
        # annotation_path = str + '/annotations/annotations.csv'
        # bbox_gt = generateBBoxGT(annotation_path,img)
        bbox_gt, width, height = generateBBoxGT(str + '/annotations/' + os.path.splitext(img)[0] + '.xml')
        bbox_pre34 = mergeCAM(bbox_pre3, bbox_pre4)
        ##bbox_pre3a4a = mergeCAM(bbox_pre3a, bbox_pre4a)  # scam apriori with apriori dcam

        ##bbox_pre33a = mergeCAM(bbox_pre3, bbox_pre3a)
        ##bbox_pre34a = mergeCAM(bbox_pre3, bbox_pre4a)  # scam with apriori dcam
        # bbox_pre334 = mergeCAM(bbox_pre3, bbox_pre334)  # scam apriori with apriori dc
        ##bbox_pre33a4a = mergeCAM(bbox_pre3, bbox_pre3a4a)

        ## bbox_pre43a = mergeCAM(bbox_pre4, bbox_pre3a)
        ## bbox_pre3a4 = mergeCAM(bbox_pre3a, bbox_pre4)
        ## bbox_pre44a = mergeCAM(bbox_pre4, bbox_pre4a)
        ## bbox_pre3a4a4 = mergeCAM(bbox_pre3a4a, bbox_pre4)
        ## bbox_pre43a4a = mergeCAM(bbox_pre4, bbox_pre3a4a)
        #
        ## bbox_pre3a34 = mergeCAM(bbox_pre3a, bbox_pre34)
        ## bbox_pre344a = mergeCAM(bbox_pre34, bbox_pre4a)
        #
        ## bbox_pre4a34 = mergeCAM(bbox_pre4a, bbox_pre34)
        ## bbox_pre343a4a = mergeCAM(bbox_pre34, bbox_pre3a4a)

        # cv2.imshow('image', bbox_pre34)
        # cv2.waitKey(0)
        # ar3 = numpy.array(bbox_pre34)
        # print(type(ar3))
        # print(bbox_pre34)
        bbox_list = [bbox_pre3, bbox_pre4, bbox_pre34]
        # bbox_list = [bbox_pre3, bbox_pre4, bbox_pre3a, bbox_pre4a, bbox_pre34, bbox_pre3a4a, bbox_pre33a, bbox_pre34a,
        #              bbox_pre33a4a, bbox_pre43a, bbox_pre3a4, bbox_pre44a, bbox_pre43a4a, bbox_pre3a4a4, bbox_pre3a34,
        #              bbox_pre4a34, bbox_pre344a, bbox_pre343a4a]

        common_bbox_test = []
        for i, bbox in enumerate(bbox_list):
            value_temp, t = comparePretoGt(bbox, bbox_gt)
            common_bbox_test.append(t)
            TP[i] = TP[i] + value_temp[0]
            FP[i] = FP[i] + value_temp[1]
            FN[i] = FN[i] + value_temp[2]

        with open(box_file, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            for obj in bbox_pre34:
                spamwriter.writerow(
                    [img, obj.x1/width, obj.y1/height, obj.x2/width, obj.y2/height, obj.confidence])

        with open(gt_file, 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            for obj in bbox_gt:
                spamwriter.writerow([img, obj.x1/width, obj.y1/height, obj.x2/width, obj.y2/height])

        # BBox_num = BBox_num + len(bbox_gt)
        # preBBox_num = preBBox_num + len(bbox_pre34)

        # visulize result
        # rr = [bbox_pre3, bbox_pre4, bbox_pre34]

        i = 0
        for k, loc in zip(bbox_list, folder):
            # print(os.path.join(store_path, loc))
            print(store_path + loc + img)
            vi_img = cv2.imread(str + '/img/' + img)
            vi_img = drawRect(vi_img, bbox_gt, (255, 0, 0))  # Blue
            vi_img = drawRect(vi_img, k, (255, 255, 255))  # White
            # if not os.path.exists(os.path.join(store_path, loc)): os.makedirs(os.path.join(store_path, loc))
            cv2.imwrite(store_path + loc + img, vi_img)
            i = i + 1
        #
        # cv2.imshow('t', vi_img)
        # cv2.waitKey(5500)

        corrects += torch.sum(preds == 1)
        test_data_size = test_data_size + 1

    print('{:.2f}'.format(corrects / test_data_size))

    for i in range(len(bbox_list)):
        print(folder[i])
        print('TP: {:.0f} FP: {:.0f} FN: {:.0f}'.format(TP[i], FP[i], FN[i]))
        print('Precision : {:.4f}  Recall : {:.4f}'.format(TP[i] / (TP[i] + FP[i]), TP[i] / (TP[i] + FN[i])))
        print()

    # print 'BBox_num: {:.0f} preBBox_num: {:.0f}'.format(BBox_num, preBBox_num)
    return [corrects / test_data_size, TP, FP, FN]


if __name__ == "__main__":
    store_path = r'D:\CODE_AND_RESULTS\new_methods\utils\no_DA'
    path = r'D:\CODE_AND_RESULTS\new_methods\utils\model_trained\\final_models\\l1params_single2_'
    select_model = 'CBAM'
    # select_model = 'DA_PAM'
    methods = ['all']
    K = [4]  # correct
    # COS = [0.01, 0.02, 0.1, 0.5, 0.7] #correct
    COS = [0.02]
    CA = []
    TA = []
    FA = []
    PA = []

    cam = False
    pam = False
    result_path = 'D:\\CODE_AND_RESULTS\\new_methods\\utils\\no_DA\\final_result'
    file = os.path.join(result_path, f'result_cbam_l1.csv')
    box_file = os.path.join(result_path, f'cbam_l1_new_bbox_modif_wsaddr.csv')
    gt_file = os.path.join(result_path, f'cbam_l1_new_gt_modif_wsaddr.csv')
    with open(file, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        ## spamwriter.writerow(['box_name', 'method', 'K', 'COS', 'TP', 'FP', 'FN', 'Precison', 'Recall', 'cls_res'])
        spamwriter.writerow(['box_name', 'method', 'TP', 'FP', 'FN', 'Precison', 'Recall', 'cls_res'])

        # for method in methods:
        #     if method == 'all':
        #         cam = True
        #         pam = True
        #     if method == 'pam':
        #         pam = True
        #     if method == 'cam':
        #         cam = True
        #     count = 0
        #     for k in K:
        #         for cos in COS:

                    # model_path = path + select_model + '_' + str(cos) + '_' + str(k) + '_0_' + method+'.pkl'  #correct
                    # model_path = path + select_model + '_' + str(cos) + '_' + str(k) + '.pkl'  # trial
                    # load model
                    # from new_methods.model.resnet_DA_PAM import model
        model_path = path + select_model + '_' + '.pkl'  # correct

        from new_methods.model.cbam import model

        model_ft = model(pretrained=True, num_classes=2)
        # model_ft = model(pretrained=True, num_classes=2, num_maps=k, cos_alpha=cos, pam=pam, cam=cam)
        model_ft = model_ft.to(device)
        model_ft.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        ##final_path = os.path.join(store_path, method, str(k) + '_' + str(cos))
        final_path = os.path.join(store_path)

        for t in [x[1:-1] for x in folder]:
            temp = os.path.join(final_path, t)
            # print(temp)
            if not os.path.exists(temp):
                os.makedirs(temp)
        # exit(0)

        # print(final_path)
        res = test(model_ft, final_path, box_file, gt_file)
        for i in range(3):
            # spamwriter.writerow(
                # [bbox_list_name[i], str(method), str(k), str(cos), res[1][i], res[2][i], res[3][i],
                #  res[1][i] / (res[1][i] + res[2][i]), res[1][i] / (res[1][i] + res[3][i]),
                #  res[0]])
            spamwriter.writerow(
                 [bbox_list_name[i], res[1][i], res[2][i], res[3][i],
                  res[1][i] / (res[1][i] + res[2][i]), res[1][i] / (res[1][i] + res[3][i]),
                   res[0]])
            pass
        # count = count + 1
        # CA.append(count)
        # PA.append(res[0])
        # TA.append(res[1])
        # FA.append(res[2])

        # show(CA, TA, FA, PA)
        # CA = []
        # PA = []
        # TA = []
        # FA = []
        pam = False
        cam = False
